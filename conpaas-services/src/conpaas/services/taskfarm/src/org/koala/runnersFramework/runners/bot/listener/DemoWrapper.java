package org.koala.runnersFramework.runners.bot.listener;

import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import org.koala.runnersFramework.runners.bot.BagOfTasks;
import org.koala.runnersFramework.runners.bot.Job;

class DemoWrapper {

    private final State serviceState;
    private final Object lock;
    private final Timer t;
    private long samplingStartTime, samplingFinishTime;
    private long executionStartTime, executionFinishTime;
    private int noTotalTasks, noCompletedTasks;
    private double samplingPhaseTime = 20000; // ms
    private double samplingPercentage = 0.4;
    private double timePerTask;

    public DemoWrapper() {
        serviceState = new State(State.RUNNING);
        lock = new Object();
        t = new Timer();
    }

    class SamplingTask extends TimerTask {

        @Override
        public void run() {
            synchronized (lock) {
                samplingFinishTime = System.currentTimeMillis();
                serviceState.state = org.koala.runnersFramework.runners.bot.listener.State.RUNNING;
            }
        }
    }

    class ExecutionTask extends TimerTask {

        @Override
        public void run() {
            synchronized (lock) {
                executionFinishTime = System.currentTimeMillis();
                serviceState.state = org.koala.runnersFramework.runners.bot.listener.State.RUNNING;
            }
        }
    }

    MethodReport start_sampling(String inputFile) {
        synchronized (lock) {
            if (State.ADAPTING.equals(serviceState.state)) {
                return new MethodReportError("Sampling failed! Service already running.");
            }
            serviceState.state = State.ADAPTING;
        }
        // reusing some old code.
        BagOfTasks bot = new BagOfTasks(inputFile);
        ArrayList<Job> list = bot.getBoT();
        if (list == null || list.isEmpty()) {
            synchronized (lock) {
                serviceState.state = org.koala.runnersFramework.runners.bot.listener.State.RUNNING;
                return new MethodReportError("No tasks found.");
            }
        }

        noTotalTasks = list.size();
        timePerTask = samplingPhaseTime / (samplingPercentage * noTotalTasks);
        samplingStartTime = System.currentTimeMillis();
        samplingFinishTime = 0;

        t.schedule(new SamplingTask(), (long) samplingPhaseTime);
        return new MethodReportSuccess("Sampling started.");
    }

    MethodReport start_execution() {
        synchronized (lock) {
            if (State.ADAPTING.equals(serviceState.state)) {
                return new MethodReportError("Sampling failed! Service already running.");
            }
            serviceState.state = State.ADAPTING;
        }
        executionStartTime = System.currentTimeMillis();
        executionFinishTime = 0;

        double executionPhaseTime = timePerTask * (1 - samplingPercentage) * noTotalTasks;
        t.schedule(new ExecutionTask(), (long) executionPhaseTime);
        return new MethodReportSuccess("Execution started.");
    }

    MethodReport get_log() {
        // demo version can live without this implementation.
        return new MethodReportSuccess("");
    }

    MethodReport terminate_workers() {
        //nothing required over here, since no workers are actually started.
        return new MethodReportSuccess("Ok.");
    }

    State get_service_info() {
        return serviceState;
    }

    Object get_sampling_result() {
        List<SamplingResult> list = new ArrayList<SamplingResult>();
        List<String> sched = new ArrayList<String>();
        sched.add("\t" + 30 + "\t" + 40 + "\t" + 20);
        sched.add("\t" + 30 + "\t" + 34 + "\t" + 24);
        sched.add("\t" + 30 + "\t" + 29 + "\t" + 30);
        sched.add("\t" + 30 + "\t" + 22 + "\t" + 32);
        sched.add("\t" + 30 + "\t" + 21 + "\t" + 33);
        SamplingResult sr = new SamplingResult("1873477324884", sched);
        list.add(sr);
        return list;
    }

    int get_tasks_done() {
        long currTime = System.currentTimeMillis();
        synchronized (lock) {
            if (State.ADAPTING.equals(serviceState.state)) {
                // service is either in sampling or execution phase
                if (samplingFinishTime == 0) {
                    noCompletedTasks = (int) ((double) (currTime - samplingStartTime) / timePerTask);
                } else {
                    noCompletedTasks = (int) (samplingPercentage * noTotalTasks
                            + (currTime - executionStartTime) / timePerTask);
                }
            } else {
                // service is idle
                if (samplingFinishTime == 0) {
                    return 0;
                } else if (executionFinishTime == 0) {
                    noCompletedTasks = (int) (samplingPercentage * noTotalTasks);
                } else {
                    noCompletedTasks = noTotalTasks;
                }
            }
            return noCompletedTasks;
        }

    }

    int get_total_no_tasks() {
        return this.noTotalTasks;
    }

    double get_money_spent() {
        // assume in 1 atu, X jobs are finished.
        // and that there are N machines running.
        // then the money spent = 
        // ceil( (tasksCompleted * timePerTask / N) / atu ) * costperatu
        int atu = 20;
        int N = 5;
        double costPerAtu = 3;
        return Math.ceil(get_tasks_done() * timePerTask / N / atu) * costPerAtu;
    }
}