import random

def returnArrivalTime(e):
    return e[2]

def generateProcesses(numOfJobs, joblist):
    for jobnum in range(0,numOfJobs):
        pid = jobnum + 5
#        arrivalTime = 0
        arrivalTime = int(10 * random.random()) + 1
        burstTime = int(10 * random.random()) + 1
        joblist.append([pid, jobnum, arrivalTime, burstTime])
        print('[PID', str(pid), '] Job', jobnum, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')
    print('\n')          
    return joblist

def printExecTrace(joblist):
    time = 0
    print('Execution trace:')
    for job in joblist:
        print('  [ time %3d ] Run job %d for %.2f secs ( DONE at %.2f )' % (time, job[1], job[3], time + job[3]))
        time += job[3]   
    print('\n')

def computeStats(joblist):
    #Initiate needed variables
    time       = 0.0
    count      = 0
    responseTotal   = 0.0
    turnaroundTotal = 0.0
    waitTotal       = 0.0
    
    for temp in joblist:
        jobnum  = temp[1]
        burstTime = temp[3]

        response   = time
        turnaround = time + burstTime
        wait       = time

        print('  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (jobnum, response, turnaround, wait))

        responseTotal   += response
        turnaroundTotal += turnaround
        waitTotal       += wait
        time += burstTime
        count = count + 1

    avgResponseTime = responseTotal/count
    avgTurnaroundTime = turnaroundTotal/count
    avgWaitTime = waitTotal/count

    print('\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (avgResponseTime, avgTurnaroundTime, avgWaitTime))

    return [avgResponseTime, avgTurnaroundTime, avgWaitTime]
    
def main():
    joblist = []
    avgStats = []
    joblist = generateProcesses(5,joblist)
    joblist.sort(key=returnArrivalTime)
    printExecTrace(joblist)
    avgStats = computeStats(joblist)

#Run Main Function
main()