import subprocess
from hadoop.config.hadoop_settings import settings

def run_hdfs_command(args):
    cmd = ["hdfs", "dfs"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"HDFS Command Failed: {e.cmd}")
        print(f"Error: {e.stderr}")
        return None
    except FileNotFoundError:
        print("HDFS executable not found. Ensure Hadoop is installed and in PATH.")
        return None

def setup_directories():
    print("Setting up HDFS directories...")
    run_hdfs_command(["-mkdir", "-p", settings.HDFS_RAW_PATH])
    run_hdfs_command(["-mkdir", "-p", settings.HDFS_PROCESSED_PATH])
    run_hdfs_command(["-mkdir", "-p", settings.HDFS_OUTPUT_PATH])

def upload_data(local_path, hdfs_filename):
    print(f"Uploading {local_path} to HDFS...")
    hdfs_dest = f"{settings.HDFS_RAW_PATH}/{hdfs_filename}"
    run_hdfs_command(["-put", "-f", local_path, hdfs_dest])
    return hdfs_dest
