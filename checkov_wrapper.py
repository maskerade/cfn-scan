import subprocess
from checkov.main import run


#list_files = subprocess.run(["ls", "-l"])

checkov_run = subprocess.run (["checkov", "-f", "s3noecryption.yaml", "--quiet", "--compact", "--output", "cli", "-c", "CKV_AWS_19"], capture_output=True)
print("The exit code was: %d" % checkov_run.returncode)
print("The output was: %s" % checkov_run.stdout)

#run(banner="Bannertime",argv=[ "-f", "s3noecryption.yaml", "--quiet", "--compact", "--output", "cli", "-c", "CKV_AWS_19"])

run()



#checkov -f s3noecryption.yaml --quiet --compact --output  cli -c CKV_AWS_19