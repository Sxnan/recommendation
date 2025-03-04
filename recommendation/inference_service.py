# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import queue
import random
import threading
import time
from concurrent import futures
import grpc
import tensorflow as tf
from recommendation.data import SampleData, ColourData
from recommendation.code.r_model import RecommendationModel
from recommendation.proto.service_pb2 import RecordRequest, RecordResponse
from recommendation.proto.service_pb2_grpc import InferenceServiceServicer, add_InferenceServiceServicer_to_server
from recommendation.app.agent_client import AgentClient
from recommendation import db

threshold = 0.3


class ModelInference(object):
    def __init__(self, checkpoint_dir):
        self.checkpoint_dir = checkpoint_dir
        m = RecommendationModel(colour_count=128, recommend_num=6, user_count=100, country_count=20)
        record = tf.placeholder(dtype=tf.string, name='record', shape=[None])

        def multiply_split(value):
            tmp = tf.strings.to_number(tf.sparse.to_dense(tf.string_split(value, sep=',')), tf.int32)
            return tmp

        def parse_csv(value):
            columns_ = tf.decode_csv(value,
                                     record_defaults=[0, 0, '0,0,0,0,0,0', 0, '0,0,0,0,0,0', 0], field_delim=' ')
            return columns_[0], columns_[1], multiply_split(columns_[2]), columns_[3], multiply_split(columns_[4]), \
                   columns_[5]

        columns = parse_csv(record)

        features = {'user': columns[0], 'country': columns[1],
                    'recommend_colours_1': columns[2],
                    'click_colour_1': columns[3],
                    'recommend_colours_2': columns[4], 'click_colour_2': columns[5]}
        fs = m.features(features)
        last_layer = m.forward(fs)
        self.top_indices, self.top_values = m.output(last_layer)
        self.top_1_indices, self.top_1_values = m.top_one_output(last_layer)
        global_step = tf.train.get_or_create_global_step()
        self.mon_sess = tf.train.MonitoredTrainingSession(checkpoint_dir=checkpoint_dir)

    def inference(self, record):
        indices_res, values_res = self.mon_sess.run([self.top_indices, self.top_values], feed_dict={'record:0': record})
        results = []
        for r in indices_res:
            r = sorted(r)
            r = ','.join(map(lambda x: str(x), r))
            results.append(r)
        return results

    def inference_click(self, record):
        print(record)
        indices_res, values_res = self.mon_sess.run([self.top_1_indices, self.top_1_values], feed_dict={'record:0': record})
        results = []
        if isinstance(indices_res, list):
            for i in range(len(indices_res)):
                if values_res[i] > threshold:
                    results.append(indices_res[i])
                else:
                    results.append(-1)
        else:
            if values_res > threshold:
                results.append(indices_res)
            else:
                results.append(-1)
        return results

    def close(self):
        self.mon_sess.close()


class InferenceUtil(object):
    def __init__(self, checkpoint_dir):
        self.user_dict = SampleData.load_user_dict()
        self.queue = queue.Queue(maxsize=500)
        self.colour_data = ColourData(count=128, select_count=6)
        self.checkpoint_dir = checkpoint_dir
        self.mi = None
        self.agent_client = None

    def random_click_record(self):
        c1, c2 = self.colour_data.random_colours()
        return sorted(c1), c2[0]

    def init_model(self):
        self.mi = ModelInference(self.checkpoint_dir)

    def get_client(self):
        if self.agent_client is None:
            self.agent_client = AgentClient('localhost:30001')
        return self.agent_client

    @db.provide_session
    def init_user_cache(self, session=None):
        for k, v in self.user_dict.items():
            user = db.User()
            user.uid = k
            user.country = v
            user = session.query(db.User).filter(db.User.uid == k).first()
            if user is None:
                user = db.User()
                user.uid = k
                user.country = v
                session.add(user)
            else:
                user.country = v
            session.commit()
        for i in range(len(self.user_dict)):
            cc = []
            for j in range(2):
                r, c = self.random_click_record()
                r = ','.join(map(lambda x: str(x), r))
                cc.append((r, c))
            user_click = session.query(db.UserClick).filter(db.UserClick.uid == i).first()
            if user_click is None:
                user_click = db.UserClick()
                user_click.uid = i
                user_click.fs_1 = cc[0][0] + ' ' + str(cc[0][1])
                user_click.fs_2 = cc[1][0] + ' ' + str(cc[1][1])
                session.add(user_click)
            else:
                user_click.fs_1 = cc[0][0] + ' ' + str(cc[0][1])
                user_click.fs_2 = cc[1][0] + ' ' + str(cc[1][1])
            session.commit()

    def init(self):
        self.init_model()
        self.init_user_cache()

    def build_features(self, uid):
        record = []
        record.append(uid)
        record.append(self.user_dict[uid])
        user_click = db.get_user_click_info(uid)
        record.append(user_click.fs_1)
        record.append(user_click.fs_2)
        return ' '.join(map(lambda x: str(x), record))

    def inference(self, features):
        return self.mi.inference(features)

    def update_state(self, uid, inference_result, click_result):
        db.update_user_click_info(uid=uid, fs=inference_result + ' ' + str(click_result))

    def process_request(self, uid):
        features = self.build_features(uid)
        inference_result = self.inference([features])
        return inference_result


class InferenceService(InferenceServiceServicer):
    def __init__(self, util: InferenceUtil):
        self.util: InferenceUtil = util

    def inference(self, request, context):
        res = self.util.process_request(int(request.record))
        return RecordResponse(record=res[0])


class InferenceServer(object):
    def __init__(self, checkpoint_dir):
        db.init_db(uri='mysql://root:chen@localhost:3306/user_info')
        self.inference_util = InferenceUtil(checkpoint_dir)
        self.inference_util.init_user_cache()
        self.inference_util.init_model()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_InferenceServiceServicer_to_server(InferenceService(self.inference_util), self.server)
        self.server.add_insecure_port('[::]:' + str(30002))
        self._stop = threading.Event()

    def start(self):
        self.server.start()
        try:
            while not self._stop.is_set():
                self._stop.wait(3600)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.server.stop(grace=True)


if __name__ == '__main__':
    inference_model_dir = '/tmp/model/2'

    # inference_util = InferenceUtil(inference_model_dir)
    # inference_util.init_user_cache()
    # inference_util.init_model()
    # res = inference_util.build_features(1)
    # res = inference_util.inference([res])
    # print(res)
    is_ = InferenceServer(inference_model_dir)
    is_.start()
