iface_name = 'enp6s0f1'
id_rsa_location = '/users/seba/.ssh/id_rsa'
App_path = '/users/seba/Spark_App'
App_destination = 'seba@node0:~/Spark_App'
master_node_ip = '10.10.1.1'
nodes = ['node1', 'node2', 'node3', 'node4', 'node5']
nodes_ip = ['10.10.1.2', '10.10.1.3', '10.10.1.4', '10.10.1.5', '10.10.1.6']

setup_commands = {
    'node1':  "cd  /users/seba/spark/sbin/ ; bash start-master.sh -i 10.10.1.2 ",
    'node2':  "cd /users/seba/spark/sbin/ ; bash start-worker.sh spark://10.10.1.2:7077 ",
    'node3':  "cd /users/seba/spark/sbin/ ; bash start-worker.sh spark://10.10.1.2:7077 ",
    'node4':  "cd /users/seba/spark/sbin/ ; bash start-worker.sh spark://10.10.1.2:7077 ",
    'node5':  "cd /users/seba/spark/sbin/ ; bash start-worker.sh spark://10.10.1.2:7077 "
}

run_program_commands = {
    'node1': "cd /users/seba/spark/ ; ./bin/spark-submit --class org.apache.spark.examples.JavaWordCount --master spark://10.10.1.2:7077 --total-executor-cores 4 --executor-memory 4G --conf spark.mesos.role=dev examples/target/original-spark-examples_2.12-3.5.0-SNAPSHOT.jar alice.txt "
}

clean_up_commands = {
'node1': "cd /users/seba/spark/sbin/ ; bash stop-all.sh",
'node2': "cd /users/seba/spark/sbin/ ; bash stop-all.sh",
'node3': "cd /users/seba/spark/sbin/ ; bash stop-all.sh",
'node4': "cd /users/seba/spark/sbin/ ; bash stop-all.sh",
'node5': "cd /users/seba/spark/sbin/ ; bash stop-all.sh",
}
    

Application_logs_path = {
    'node1': '/users/seba/spark/logs/',
    'node2': '/users/seba/spark/logs/',
    'node3': '/users/seba/spark/logs/',
    'node4': '/users/seba/spark/logs/',
    'node5': '/users/seba/spark/logs/'

}


