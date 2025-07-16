import random

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
    print('Execution trace:')
    turnaround = {}
    response = {}
    lastran = {}
    wait = {}
    quantum  = 1.0
    jobcount = len(joblist)

    for i in range(0,jobcount):
        lastran[i] = 0.0
        wait[i] = 0.0
        turnaround[i] = 0.0
        response[i] = -1

    templist = []
    for e in joblist:
        templist.append(e)

    runlist = []
    runlist.append(templist[0])
    templist.pop(0)

    thetime  = 0.0
    while jobcount > 0:  
        if len(runlist) != 0:
            jobnum =  runlist[0][1]
            if response[runlist[0][1]] == -1:
                response[runlist[0][1]] = thetime

            currwait = thetime - lastran[runlist[0][1]]
            wait[runlist[0][1]] += currwait

        if len(runlist) == 0:
            ranfor = quantum
            print('  [ time %3d ] CPU idle for %.2f secs' % (thetime, ranfor))
        elif runlist[0][3] > quantum:
            runlist[0][3] -= quantum
            ranfor = quantum
            print('  [ time %3d ] Run job %3d for %.2f secs' % (thetime, runlist[0][1], ranfor))
            
        elif runlist[0][3] <= quantum:
            ranfor = runlist[0][3]
            print('  [ time %3d ] Run job %3d for %.2f secs ( DONE at %.2f )' % (thetime, runlist[0][1], ranfor, thetime + ranfor))
            turnaround[runlist[0][1]] = thetime + ranfor
            runlist.pop(0)
            jobcount -= 1
            
            
        thetime += ranfor
        lastran[jobnum] = thetime

        index = 0
        for e in templist:
            if thetime >= e[2]:
                if len(runlist) == 0:
                    runlist.append(templist[index])
                    templist.pop(index)
                    runlist = sorted(runlist, key=lambda b: b[3])
                    break
                elif runlist[0][3] >= e[3]:
                    runlist.append(templist[index])
                    templist.pop(index)
                    runlist = sorted(runlist, key=lambda b: b[3])
                    break



            # if len(runlist) == 0 and len(templist) >= 1:
            #     runlist.append(templist[index])
            #     templist.pop(index)
            #     runlist = sorted(runlist, key=lambda b: b[3])
            #     break
            # elif thetime >= e[2]:
            #     if runlist[0][3] >= e[3]:
            #         runlist.append(templist[index])
            #         templist.pop(index)
            #         runlist = sorted(runlist, key=lambda b: b[3])
            #         break

            index+=1

    
    print('\nFinal statistics:')

    turnaroundTotal = 0.0
    waitTotal       = 0.0
    responseTotal   = 0.0

    for i in range(0,len(joblist)):
        turnaroundTotal += turnaround[i]
        responseTotal += response[i]
        waitTotal += wait[i]
        print('  Job %3d -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f' % (i, response[i], turnaround[i], wait[i]))

    count = len(joblist)
    avgResponseTime = responseTotal/count
    avgTurnaroundTime = turnaroundTotal/count
    avgWaitTime = waitTotal/count
    
    print('\n  Average -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (avgResponseTime, avgTurnaroundTime, avgWaitTime))
    
def main():
    joblist = []
    avgStats = []
    joblist = generateProcesses(5,joblist)
    joblist = sorted(joblist, key=lambda e: (e[2], e[3]))
    printExecTrace(joblist)

#Run Main Function
main()