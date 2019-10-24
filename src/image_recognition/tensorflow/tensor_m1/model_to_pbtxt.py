import tensorflow as tf

graph_fn = "./tmp/output_graph.pb"

with tf.gfile.GFile(graph_fn, "rb") as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.train.write_graph(graph_def, './', './tmp/output.pbtxt', True)