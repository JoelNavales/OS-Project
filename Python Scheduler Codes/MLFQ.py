import random
import sys

def FindQueue():
    q = hiQueue
    while q < 4:
        if len(queue[q]) > 0:
            return q
        q += 1
    if len(queue[3]) > 0:
        return 3
    return -1

def Abort(str):
    sys.stderr.write(str + '\n')
    exit(1)

numQueues = 4
timeSlice = 2

quantum = {}
for i in range(numQueues):
        quantum[i] = int(timeSlice)

allotmentSlice = 1
allotment = {}
for i in range(numQueues):
    allotment[i] = int(allotmentSlice)

hiQueue = 0
ioDone = {}

numOfJobs = 5
joblist = {}
#def generateProcesses(numOfJobs, joblist):
for jobnum in range(0,numOfJobs):
    pid = jobnum + 5
#        arrivalTime = 0
    arrivalTime = int(10 * random.random()) + 1
    burstTime = int(10 * random.random()) + 1

    joblist[jobnum] = {'currPri':hiQueue, 'ticksLeft':quantum[hiQueue],
                    'allotLeft':allotment[hiQueue], 'startTime':arrivalTime,
                    'runTime':burstTime, 'timeLeft':burstTime, 'firstRun':-1, 'pid': pid} 
    if arrivalTime not in ioDone:
        ioDone[arrivalTime] = []
    ioDone[arrivalTime].append((jobnum, 'JOB BEGINS'))
    
    print('[PID', str(pid), '] Job', jobnum, '[Arrival Time:', str(arrivalTime), '| Burst Time: ', str(burstTime), ']')
#    print('\n') 
#    return joblist


# initialize the MLFQ queues
queue = {}
for q in range(numQueues):
    queue[q] = []

# TIME IS CENTRAL
currTime = 0

# use these to know when we're finished
totalJobs    = len(joblist)
finishedJobs = 0

print('\nExecution Trace:\n')

while finishedJobs < totalJobs:
    if currTime in ioDone:
        for (j, type) in ioDone[currTime]:
            q = joblist[j]['currPri']
            joblist[j]['doingIO'] = False
            print('[ time %d ] %s by JOB %d' % (currTime, type, j))
            if type == 'JOB BEGINS':
                queue[q].append(j)
            else:
                queue[q].insert(0, j)

    currQueue = FindQueue()
    if currQueue == -1:
        print('[ time %d ] IDLE' % (currTime))
        currTime += 1
        continue

    currJob = queue[currQueue][0]
    if joblist[currJob]['currPri'] != currQueue:
        Abort('currPri[%d] does not match currQueue[%d]' % (joblist[currJob]['currPri'], currQueue))

    joblist[currJob]['timeLeft']  -= 1
    joblist[currJob]['ticksLeft'] -= 1

    if joblist[currJob]['firstRun'] == -1:
        joblist[currJob]['firstRun'] = currTime

    burstTime   = joblist[currJob]['runTime']
    ticksLeft = joblist[currJob]['ticksLeft']
    allotLeft = joblist[currJob]['allotLeft']
    timeLeft  = joblist[currJob]['timeLeft']

    print('[ time %d ] Run JOB %d at PRIORITY %d [ TICKS %d ALLOT %d TIME %d (of %d) ]' % \
          (currTime, currJob, currQueue, ticksLeft, allotLeft, timeLeft, burstTime))

    if timeLeft < 0:
        Abort('Error: should never have less than 0 time left to run')


    # UPDATE TIME
    currTime += 1

    # CHECK FOR JOB ENDING
    if timeLeft == 0:
        print('[ time %d ] FINISHED JOB %d' % (currTime, currJob))
        finishedJobs += 1
        joblist[currJob]['endTime'] = currTime
        # print('BEFORE POP', queue)
        done = queue[currQueue].pop(0)
        # print('AFTER POP', queue)
        assert(done == currJob)
        continue

    if ticksLeft == 0:
        desched = queue[currQueue].pop(0)
        assert(desched == currJob)

        joblist[currJob]['allotLeft'] = joblist[currJob]['allotLeft'] - 1

        if joblist[currJob]['allotLeft'] == 0:
            # this job is DONE at this level, so move on
            if currQueue < 3:
                # in this case, have to change the priority of the job
                joblist[currJob]['currPri']   = currQueue + 1
                joblist[currJob]['ticksLeft'] = quantum[currQueue+1]
                joblist[currJob]['allotLeft'] = allotment[currQueue+1]
                queue[currQueue+1].append(currJob)

            else:
                joblist[currJob]['ticksLeft'] = quantum[currQueue]
                joblist[currJob]['allotLeft'] = allotment[currQueue]
                queue[currQueue].append(currJob)

        else:
            # this job has more time at this level, so just push it to end
            joblist[currJob]['ticksLeft'] = quantum[currQueue]
            queue[currQueue].append(currJob)

# print out statistics
print('')
print('Final statistics:')
responseSum   = 0
turnaroundSum = 0
for i in range(numOfJobs):
    response   = joblist[i]['firstRun'] - joblist[i]['startTime']
    turnaround = joblist[i]['endTime'] - joblist[i]['startTime']
    print('  Job %2d: startTime %3d - response %3d - turnaround %3d' % (i, joblist[i]['startTime'], response, turnaround))
    responseSum   += response
    turnaroundSum += turnaround

print('\n  Avg %2d: startTime n/a - response %.2f - turnaround %.2f' % (i, float(responseSum)/numOfJobs, float(turnaroundSum)/numOfJobs))
print('\n')