import os
import subprocess

def SubmitTorque(JobString, JobID = None, Mem = 512):
    '''
    Submits a job to a Torque scheduler using qsub. Takes as input
    a string representing the contents of the job script file. This
    string defines a Linux command line call to Python that invokes a
    function and passes command line arguments using the -c python
    argument. The job string is specific to the algorithm/function
    and is generated by a separate script that interprets parameter
    values and generates the job string.
    *Inputs:
    String (string) - Formatted string to invoke python function
                        defining arguments.
    JobID (string) - string to assign name to job in PBS scheduler
                    (-N option).
    Mem (scalar) - free memory parameter for 'mem_free', in MB, as
                    defined by qsub.
    *Outputs:

    *Related Functions:
    '''

    #create job file in working directory
    Script = open('/Users/lcoop22/Desktop/job.sh', 'w');

    #add command to CD to working directory
    Script.write('cd #PBS_O_WORKDIR\n')

    #print command to file
    if JobString[-1] != '\n':
        JobString = JobString + '\n'
    Script.write(JobString)

    #print wait command to job file
    Script.write('wait $(ps | grep python | awk ''{print $2}'') && cat %s ' + JobID + '.txt\n')

    #close job file
    Script.close()

    #submit job through qsub via system call
    if(JobString is None): #submit job without -N option
        try:
            subprocess.check_output('qsub -q matlab -o /dev/null -e /dev/null -V -l mem=' + str(Mem) + ' job.sh', stderr = subprocess.STDOUT, shell = True)
        except subprocess.CalledProcessError as error:
            Result = error
    else: #submit job with -N option
        if(not JobID[0].isalpha()):
            JobID = '.' + JobID
        try:
            subprocess.check_output('qsub -q matlab -o /dev/null -e /dev/null -V -l mem=' + str(Mem) + ' -N ' + JobID + ' job.sh', stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as error:
            Result = error

    #delete job file
    os.remove('job.sh')

    #return output
    return(Result)
