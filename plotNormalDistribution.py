import subprocess
import numpy as np
import rospy
import tf
import visualization_msgs.msg as visualization_msgs
from tqdm import tqdm

import numpy as np
import rospy
import visualization_msgs.msg as visualization_msgs
import tf.transformations as tf
from scipy.spatial.transform import Rotation

def publish_ndt_map_marker(num_of_covs, means, covs, pub):
    marker_array = visualization_msgs.MarkerArray()
    for i in range(num_of_covs):
        cov = np.array(covs[i])
        mean = means[i]
        evals, evecs = np.linalg.eigh(cov)
        orient =  np.array(evecs)
        q = Rotation.from_matrix(orient).as_quat()

        marker = visualization_msgs.Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time()
        marker.ns = "NDT"
        marker.id = i
        marker.type = visualization_msgs.Marker.SPHERE
        marker.action = visualization_msgs.Marker.ADD
        marker.pose.position.x = mean[0]
        marker.pose.position.y = mean[1]
        marker.pose.position.z = mean[2]
        marker.pose.orientation.x = q[0]
        marker.pose.orientation.y = q[1]
        marker.pose.orientation.z = q[2]
        marker.pose.orientation.w = q[3]
        # marker.pose.orientation.x = 0
        # marker.pose.orientation.y = 0
        # marker.pose.orientation.z = 0
        # marker.pose.orientation.w = 1
        marker.scale.x = 6 * evals[0]
        marker.scale.y = 6 * evals[1]
        marker.scale.z = 6 * evals[2]
        sorted_arr = np.sort(evals)
        value = sorted_arr[0]*sorted_arr[2]/(sorted_arr[1]*sorted_arr[1])
        marker.color.a = 1
        marker.color.r = 0.2
        marker.color.g = 0.2
        marker.color.b = 0.2
        # if value < 0.1 and value > 0.01:
        #     marker.color.a = 1
        #     marker.color.r = 0.0
        #     marker.color.g = 1
        #     marker.color.b = 0.0
        # elif value >= 2.4:
        #     marker.color.a = 1
        #     marker.color.r = 0.0
        #     marker.color.g = 0.0
        #     marker.color.b = 1

        if value < 0.3:
            marker.color.a = 1
            marker.color.r = 1.0
            marker.color.g = 0
            marker.color.b = 0.0
        elif value < 0.6 and value >= 0.3:
            marker.color.a = 1
            marker.color.r = 0.0
            marker.color.g = 1
            marker.color.b = 0.0
        elif value < 0.9 and value >= 0.6:
            marker.color.a = 1
            marker.color.r = 0.0
            marker.color.g = 0.0
            marker.color.b = 1
        elif value < 1.2 and value >= 0.9:
            marker.color.a = 1
            marker.color.r = 1
            marker.color.g = 1
            marker.color.b = 0.0
        elif value < 1.5 and value >= 1.2:
            marker.color.a = 1
            marker.color.r = 0.0
            marker.color.g = 1
            marker.color.b = 1
        elif value < 1.8 and value >= 1.5: 
            marker.color.a = 1
            marker.color.r = 1
            marker.color.g = 0
            marker.color.b = 1

        marker_array.markers.append(marker)
    pub.publish(marker_array)
    rospy.loginfo("Published ndt map marker")

if __name__=='__main__':
    # 启动roscore
    roscore_process = subprocess.Popen('roscore')

    # 设置ROS_MASTER_URI环境变量
    # os.environ['ROS_MASTER_URI'] = 'http://localhost:11311'

    # 启动rviz
    rviz_process = subprocess.Popen(['rviz', '-d', 'path/to/my.rviz'])
    with open('path/to/demo.txt', 'r') as f:
        lines = f.readlines()
        means = []
        covs = []
        for i in range(0, len(lines), 6):
            mean_temp = list(map(float, lines[i+1].split()))
            mean = np.array([float(mean_temp[0]), float(mean_temp[1]), float(mean_temp[2])])
            # if(i == 0):
            #     mean1 = mean
            #     print(mean1)
            cov = [list(map(float, line.split())) for line in lines[i+3:i+6]]
            # if mean[2] < 0 or mean[2] > 4:
            #     continue
            means.append(mean)
            covs.append(cov)
        num_of_covs = len(covs)
        print(num_of_covs, len(means))
        pub = rospy.Publisher('ndt_map_marker', visualization_msgs.MarkerArray, queue_size=1)
        rospy.init_node('ndt_map_marker_node')
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            publish_ndt_map_marker(num_of_covs, means, covs, pub)
            rate.sleep()
