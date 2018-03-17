import boto3
import sys


def main(*args):
    access_key = "AKIAJX7SJ3BXPEGL2YQQ"
    secret_key = "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"
    client = boto3.client('emr', aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key, region_name='us-east-1')
    print "start"
    S3_BUCKET = 'testdsp3'
    S3_BUCKET2= 'marinatomer3'
    S3_KEY = 'spark/main.py'
    S3_URI = 's3://{bucket}/{key}'.format(bucket=S3_BUCKET, key=S3_KEY)
    # upload file to an S3 bucket


    response = client.run_job_flow(
        Name="DSP3T",
        ReleaseLabel='emr-4.8.0',
        Instances={
            'MasterInstanceType': 'm1.large',
            'SlaveInstanceType': 'm1.large',
            'InstanceCount': 4,
            'KeepJobFlowAliveWhenNoSteps': False,
            'TerminationProtected': False,
        },
        Applications=[],
        LogUri="s3://{}/logs/".format(S3_BUCKET),
        BootstrapActions=[],
        Configurations=[
            {
                "Classification": "mapred-site",
                "Properties": {
                    "mapreduce.map.memory.mb": "4096",
                    "mapred.tasktracker.map.tasks.maximum": "4",
                    "mapreduce.map.java.opts":"-Xmx1024m"
                }
            }
            ],
        Steps=[
            {
                'Name': 'Setup Debugging',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': ['state-pusher-script']
                }
            },
            {
                'Name': 'Run record reader',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': ['hadoop-streaming',
                             '-files',
                             "s3://{bucket}/word_count_mapper.py,s3://{bucket}/word_count_reducer.py".format(
                                 bucket=S3_BUCKET2),
                             '-mapper', "word_counter_mapper.py",
                             '-reducer', "word_counter_reducer.py",
                             '-input', "s3://{}/biarcs.**-of-99.gz".format(S3_BUCKET),
                             '-output', "s3://{}/output100/RECORD_READER".format(S3_BUCKET2)
                             ]
                }
            },
            {
                'Name': 'Run indexing',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': ['hadoop-streaming',
                             '-files',
                             "s3://{bucket}/word_index_mapper.py,s3://{bucket}/word_index_reducer.py".format(
                                 bucket=S3_BUCKET2),
                             '-mapper', "word_index_mapper.py",
                             '-reducer', "word_index_reducer.py",
                             '-input', "s3://{}/output100/RECORD_READER/part-*****".format(S3_BUCKET2),
                             '-output', "s3://{}/output100/INDEXING".format(S3_BUCKET2)
                             ]
                }
            },
            {
                'Name': 'Run word vector',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': ['hadoop-streaming',
                             '-files',
                             "s3://{bucket}/word_vector_mapper.py,s3://{bucket}/word_vector_reducer.py".format(
                                 bucket=S3_BUCKET2),
                             '-mapper', "word_vector_mapper.py",
                             '-reducer', "word_vector_reducer.py",
                             '-input', "s3://{}/biarcs.**-of-99.gz".format(S3_BUCKET),
                             '-output', "s3://{}/output100/WORD_VECTOR".format(S3_BUCKET2),
                             '-cacheFile', "s3://{}/word-relatedness.txt#input2.txt".format(S3_BUCKET2)
                             ]
                }
            },
            {
                'Name': 'Run four vectors',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': ['hadoop-streaming',
                             '-files',
                             "s3://{bucket}/four_vectors_mapper.py".format(
                                 bucket=S3_BUCKET2),
                             '-mapper', "four_vectors_mapper.py",
                             '-input', "s3://{}/output100/WORD_VECTOR/part-*****".format(S3_BUCKET2),
                             '-output', "s3://{}/output100/FOUR_VECTORS".format(S3_BUCKET2),
                             '-cacheFile', "s3://{}/output100/INDEXING/part-00000#input.txt".format(S3_BUCKET2)
                             ]
                }
            },
            {
                'Name': 'Run make pair',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': ['hadoop-streaming',
                             '-files',
                             "s3://{bucket}/make_pair_mapper.py,s3://{bucket}/make_pair_reducer.py".format(
                                 bucket=S3_BUCKET2),
                             '-mapper', "make_pair_mapper.py",
                             '-reducer', "make_pair_reducer.py",
                             '-input', "s3://{}/output100/FOUR_VECTORS/part-*****".format(S3_BUCKET2),
                             '-output', "s3://{}/output100/MAKE_PAIR".format(S3_BUCKET2),
                             '-cacheFile', "s3://{}/word-relatedness.txt#input3.txt".format(S3_BUCKET2)
                             ]
                }
            },
            {
                'Name': 'Run similarity',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': ['hadoop-streaming',
                             '-files',
                             "s3://{bucket}/similarity_mapper.py".format(
                                 bucket=S3_BUCKET2),
                             '-mapper', "similarity_mapper.py",
                             '-input', "s3://{}/output100/MAKE_PAIR/part-*****".format(S3_BUCKET2),
                             '-output', "s3://{}/output100/SIMILARITY".format(S3_BUCKET2),
                             ]
                }
            }
        ],
        VisibleToAllUsers=True,
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole'
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(10)