iface_name = 'enp6s0f0'
id_rsa_location = '/users/seba/.ssh/id_rsa'
App_path = '/users/seba/Spark_mesos'
App_destination = 'seba@node0:~/Spark_mesos'
master_node_ip = '10.10.1.1'
nodes = ['node1', 'node2', 'node3', 'node4', 'node5','node6']
nodes_ip = ['10.10.1.2', '10.10.1.3', '10.10.1.4', '10.10.1.5', '10.10.1.6', '10.10.1.7']

setup_commands = {
    'node2':  "cd /mydata/mesos-1.11.0/build ; screen -d -m sudo ./bin/mesos-master.sh --ip=10.10.1.3 --work_dir=/mydata/mesos-1.11.0 &",
    'node3':  "cd /mydata/mesos-1.11.0/build ; screen -d -m sudo ./bin/mesos-agent.sh --ip=10.10.1.4 --master=10.10.1.3:5050 --work_dir=/mydata/mesos-1.11.0 &",
    'node4':  "cd /mydata/mesos-1.11.0/build ; screen -d -m sudo ./bin/mesos-agent.sh --ip=10.10.1.5 --master=10.10.1.3:5050 --work_dir=/mydata/mesos-1.11.0 &",
    'node5':  "cd /mydata/mesos-1.11.0/build ; screen -d -m sudo ./bin/mesos-agent.sh --ip=10.10.1.6 --master=10.10.1.3:5050 --work_dir=/mydata/mesos-1.11.0 &",
    'node6': "cd /mydata/mesos-1.11.0/build ; screen -d -m sudo ./bin/mesos-agent.sh --ip=10.10.1.7 --master=10.10.1.3:5050 --work_dir=/mydata/mesos-1.11.0 &",
    'node1':  "cd  /users/seba/spark/sbin/ ; ./start-mesos-dispatcher.sh -m mesos://10.10.1.3:5050 --host 10.10.1.2 "
}

run_program_commands = {
    'node1': "cd /users/seba/spark/ ; ./bin/spark-submit --class org.apache.spark.examples.JavaWordCount --master mesos://10.10.1.3:5050 --executor-memory 4G examples/target/original-spark-examples_2.12-3.5.0-SNAPSHOT.jar /mydata/alice.txt"
}

clean_up_commands = { 
'node1': "cd  /users/seba/spark/sbin/ ; bash stop-mesos-dispatcher.sh",
'node2': "sudo pkill mesos",
'node3': "sudo pkill mesos",
'node4': "sudo pkill mesos",
'node5': "sudo pkill mesos",
'node6': "sudo pkill mesos"

}
    

Application_logs_path = {
    'node1': '/users/seba/spark/logs/',
    'node2': '/users/seba/spark/logs/',
    'node3': '/users/seba/spark/logs/',
    'node4': '/users/seba/spark/logs/',
    'node5': '/users/seba/spark/logs/',
    'node6': '/users/seba/spark/logs/'

}


