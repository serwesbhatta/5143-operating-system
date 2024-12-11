from time import sleep
import sys

from components import Device, Job, Queue, SystemClock, Stats
from api import getJob, init, getJobsLeft
from utils import myKwargs
import json

from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.panel import Panel


class Scheduler:
    def __init__(self, clock, cpus, ios):
        self.jobs = Queue()
        self.new_queue = Queue()
        self.ready_queue = Queue()
        self.running_queue = Queue()
        self.waiting_queue = Queue()
        self.io_queue = Queue()
        self.exit_queue = Queue()
        self.clock = clock
        self.ios = ios
        self.cpus = cpus

        # For MLFQ
        self.q1 = Queue()
        self.q2 = Queue()
        self.q3 = Queue()
        self.q4 = Queue()
        self.q5 = Queue()

        # Initialize the priority levels of the queues
        self.q1.priority = 1
        self.q2.priority = 2
        self.q3.priority = 3
        self.q4.priority = 4
        self.q5.priority = 5

        # Initialize the time slice of the queues
        self.q1.time_slice = 5
        self.q2.time_slice = 10
        self.q3.time_slice = 15
        self.q4.time_slice = 20
        self.q5.time_slice = 25

    def generate_table(self, algorithm=None):
        # Main layout
        layout = Layout()

        # Queue Table
        self.queue_table = Table(title="Job Queues")
        self.queue_table.add_column(
            "Queue", justify="center", style="cyan", no_wrap=True
        )
        self.queue_table.add_column(
            "Jobs", justify="center", style="magenta", no_wrap=True
        )

        # Populate queue table
        self.queue_table.add_row("New Queue", self.format_jobs(self.new_queue.jobs))
        self.queue_table.add_row("Ready Queue", self.format_jobs(self.ready_queue.jobs))
        self.queue_table.add_row(
            "Running Queue", self.format_jobs(self.running_queue.jobs)
        )
        self.queue_table.add_row(
            "Waiting Queue", self.format_jobs(self.waiting_queue.jobs)
        )
        self.queue_table.add_row("IO Queue", self.format_jobs(self.io_queue.jobs))
        self.queue_table.add_row("Exit Queue", self.format_jobs(self.exit_queue.jobs))

        # CPU Table
        self.cpu_table = Table(title="CPU Status")
        self.cpu_table.add_column("CPU", justify="center", style="yellow", no_wrap=True)
        self.cpu_table.add_column("Job", justify="center", style="green", no_wrap=True)

        for cpu in self.cpus:
            if cpu.is_free():
                self.cpu_table.add_row(cpu.name, Text("Idle", style="dim red"))
            else:
                self.cpu_table.add_row(cpu.name, self.format_jobs([cpu.job]))

        # IO Table
        self.io_table = Table(title="IO Devices Status")
        self.io_table.add_column(
            "IO Device", justify="center", style="blue", no_wrap=True
        )
        self.io_table.add_column("Job", justify="center", style="green", no_wrap=True)

        for io in self.ios:
            if io.is_free():
                self.io_table.add_row(io.name, Text("Idle", style="dim red"))
            else:
                self.io_table.add_row(io.name, self.format_jobs([io.job]))

        # Job Table
        self.job_table = Table(title="Job Status")
        self.job_table.add_column(
            "Job ID", justify="center", style="cyan", no_wrap=True
        )
        self.job_table.add_column(
            "Arrival Time", justify="center", style="magenta", no_wrap=True
        )
        self.job_table.add_column(
            "Priority", justify="center", style="yellow", no_wrap=True
        )
        self.job_table.add_column(
            "Burst Type", justify="center", style="green", no_wrap=True
        )
        self.job_table.add_column(
            "Burst Duration", justify="center", style="blue", no_wrap=True
        )
        if algorithm == "MLFQ" or algorithm == "RR":
            self.job_table.add_column(
                "Time Slice Remaining", justify="center", style="red", no_wrap=True
            )
        self.job_table.add_column(
            "CPU Wait Time", justify="center", style="red", no_wrap=True
        )

        for job in self.jobs.jobs:
            if algorithm == "MLFQ" or algorithm == "RR":
                self.job_table.add_row(
                    str(job.job_id),
                    str(job.arrival_time),
                    str(job.priority),
                    job.burst_type,
                    str(job.burst_duration),
                    str(job.time_slice_remaining),
                    str(job.cpu_wait_time),
                )
            else:
                self.job_table.add_row(
                    str(job.job_id),
                    str(job.arrival_time),
                    str(job.priority),
                    job.burst_type,
                    str(job.burst_duration),
                    str(job.cpu_wait_time),
                )

        if algorithm == "MLFQ":
            self.priority_queue = Table(title="Priority Queues")
            self.priority_queue.add_column(
                "Queue", justify="center", style="cyan", no_wrap=True
            )
            self.priority_queue.add_column(
                "Jobs", justify="center", style="magenta", no_wrap=True
            )

            self.priority_queue.add_row("Queue 1", self.format_jobs(self.q1.jobs))
            self.priority_queue.add_row("Queue 2", self.format_jobs(self.q2.jobs))
            self.priority_queue.add_row("Queue 3", self.format_jobs(self.q3.jobs))
            self.priority_queue.add_row("Queue 4", self.format_jobs(self.q4.jobs))
            self.priority_queue.add_row("Queue 5", self.format_jobs(self.q5.jobs))

        left_column = Layout(name="left")
        left_column.split(
            Layout(Panel(self.queue_table), ratio=5, size=None),
            Layout(Panel(self.cpu_table, title="CPU"), size=None, ratio=5),
            Layout(Panel(self.io_table, title="IO Devices"), size=None, ratio=5),
        )

        right_column = Layout(name="right")
        if algorithm == "MLFQ":
            right_column.split(
                Layout(Panel(self.job_table), ratio=7, size=None),
                Layout(
                    Panel(self.priority_queue, title="Priority Queues"),
                    size=None,
                    ratio=3,
                ),
                Layout(
                    Panel(str(self.clock.current_time), title="Clock"),
                    size=None,
                    ratio=1,
                ),
            )
        else:
            right_column.split(
                Layout(Panel(self.job_table), ratio=10, size=None),
                Layout(
                    Panel(str(self.clock.current_time), title="Clock"),
                    size=None,
                    ratio=1,
                ),
            )

        right_column["right"].ratio = 3
        left_column["left"].ratio = 2

        layout.split_row(left_column, right_column)
        return layout

    def format_jobs(self, jobs):
        """Format jobs as colorful blocks."""
        if not jobs:
            return Text("Empty", style="dim")
        return ", ".join([f"[bold cyan]Job {job.job_id}[/]" for job in jobs])

    def fetch_jobs(self, client_id, session_id, clock_time):
        """Fetches new jobs from the /jobs endpoint."""
        """Retrieves jobs arriving at the current time and places them in the new_queue."""
        response = getJob(client_id, session_id, clock_time)
        if response["success"]:
            response = response["message"]
            if response["data"]:
                for job in response["data"]:
                    job_id = job["job_id"]
                    arrival_time = job["arrival_time"]
                    priority = job["priority"]
                    new_job = Job(job_id, arrival_time, priority)
                    self.new_queue.enqueue(new_job, 0)
                    self.jobs.enqueue(new_job, 0)
        else:
            print(f"Error: {response.status_code}")
            return None

    def enqueue_priority_queue(self, job):
        for queue in [self.q1, self.q2, self.q3, self.q4, self.q5]:
            if job.priority == queue.priority:
                job.time_slice_remaining = queue.time_slice
                queue.enqueue(job)

    def move_to_ready_queue(self, client_id, session_id, algorithm=None):
        """Moves jobs from the new queue to the ready queue."""
        if algorithm == "MLFQ":
            while not self.new_queue.is_empty():
                job = self.new_queue.dequeue()
                job.get_job_burst(client_id, session_id, job.job_id)
                for queue in [self.q1, self.q2, self.q3, self.q4, self.q5]:
                    if job.priority == queue.priority:
                        job.time_slice_remaining = queue.time_slice
                        queue.enqueue(job)
            for jobs in [self.q1, self.q2, self.q3, self.q4, self.q5]:
                if not jobs.is_empty():
                    job = jobs.dequeue()
                    self.ready_queue.enqueue(job, 0)
            self.ready_queue.jobs.sort(key=lambda x: x.priority, reverse=True)
        else:
            while not self.new_queue.is_empty():
                job = self.new_queue.dequeue()
                job.get_job_burst(client_id, session_id, job.job_id)
                self.ready_queue.enqueue(job, 0)

    def process_ready_queue(self, algorithm=None,priority=False):
        """Processes the ready queue."""
        if algorithm == "MLFQ":
            for job in self.ready_queue.jobs:
                if job.cpu_wait_time == 10:
                    job.cpu_wait_time = 0
                    if job.priority > 1:
                        job.priority -= 1

                job.cpu_wait_time += 1

        for cpu in self.cpus:
            if cpu.is_free():
                if not self.ready_queue.is_empty():
                    if priority:
                        self.ready_queue.jobs.sort(
                            key=lambda x: x.priority, reverse=True
                        )
                    job = self.ready_queue.dequeue()
                    cpu.load_job(job)
                    self.running_queue.enqueue(job, 0)

    def process_waiting_queue(self):
        """Processes the waiting queue."""
        for io in self.ios:
            if io.is_free():
                if not self.waiting_queue.is_empty():
                    job = self.waiting_queue.dequeue()
                    io.load_job(job)
                    self.io_queue.enqueue(job, 0)

    def process_running_queue(
        self, client_id, session_id, algorithm, time_quantum=5, preemptive=False
    ):
        """Processes the running queue."""
        if not self.running_queue.is_empty():
            for job in self.running_queue.jobs:
                if algorithm == "FCFS":
                    job.decrement_duration()
                    if job.burst_complete():
                        for cpu in self.cpus:
                            if cpu.job and cpu.job.job_id == job.job_id:
                                cpu.free()
                        job.get_job_burst(client_id, session_id, job.job_id)
                        if job.burst_type == "IO":
                            self.waiting_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                        elif job.burst_type == "EXIT":
                            self.exit_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                            job.time_slice_remaining = None
                            job.cpu_wait_time = None
                        else:
                            self.ready_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                elif algorithm == "RR":
                    if job.time_slice_remaining is None:
                        job.time_slice_remaining = time_quantum

                    job.decrement_duration()
                    job.time_slice_remaining -= 1

                    if job.burst_complete():
                        for cpu in self.cpus:
                            if cpu.job and cpu.job.job_id == job.job_id:
                                cpu.free()
                        job.time_slice_remaining = time_quantum
                        job.get_job_burst(client_id, session_id, job.job_id)
                        if job.burst_type == "IO":
                            self.waiting_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                        elif job.burst_type == "EXIT":
                            self.exit_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                            self.time_slice_remaining = 0
                            self.cpu_wait_time = 0
                        else:
                            self.ready_queue.enqueue(job, 0)
                            self.running_queue.remove(job)

                    if job.time_slice_remaining == 0:
                        for cpu in self.cpus:
                            if cpu.job and cpu.job.job_id == job.job_id:
                                cpu.free()
                        job.time_slice_remaining = time_quantum

                        if not job.burst_complete():
                            self.ready_queue.enqueue(job, 0)
                            self.running_queue.remove(job)

            if algorithm == "PR":
                for job in self.running_queue.jobs:
                    job.decrement_duration()
                    if job.burst_complete():
                        for cpu in self.cpus:
                            if cpu.job and cpu.job.job_id == job.job_id:
                                cpu.free()
                        job.get_job_burst(client_id, session_id, job.job_id)
                        if job.burst_type == "IO":
                            self.waiting_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                        elif job.burst_type == "EXIT":
                            self.exit_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                        else:
                            self.ready_queue.enqueue(job)
                            self.running_queue.remove(job)

                if not self.ready_queue.is_empty():
                    if preemptive:
                        if not self.running_queue.is_empty():
                            highest_priority_job = min(
                                self.ready_queue.jobs, key=lambda x: x.priority
                            )

                            lowest_priority_job = max(
                                self.running_queue.jobs, key=lambda x: x.priority
                            )

                            if (
                                lowest_priority_job.priority
                                > highest_priority_job.priority
                            ):
                                for cpu in self.cpus:
                                    if (
                                        cpu.job
                                        and cpu.job.job_id == lowest_priority_job.job_id
                                    ):
                                        cpu.free()
                                        cpu.load_job(highest_priority_job)
                                self.ready_queue.enqueue(lowest_priority_job)
                                self.running_queue.remove(lowest_priority_job)
                                self.running_queue.enqueue(highest_priority_job)
                                self.ready_queue.jobs.remove(highest_priority_job)
            elif algorithm == "MLFQ":
                for job in self.running_queue.jobs:
                    job.decrement_duration()
                    job.time_slice_remaining -= 1

                    if job.burst_complete():
                        for cpu in self.cpus:
                            if cpu.job and cpu.job.job_id == job.job_id:
                                cpu.free()
                        if job.time_slice_remaining == 0:
                            if job.priority < 5:
                                job.priority += 1
                        else:
                            if job.priority > 1:
                                job.priority -= 1
                        job.get_job_burst(client_id, session_id, job.job_id)

                        for queue in [self.q1, self.q2, self.q3, self.q4, self.q5]:
                            if job.priority == queue.priority:
                                job.time_slice_remaining = queue.time_slice

                        if job.burst_type == "IO":
                            self.waiting_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                        elif job.burst_type == "EXIT":
                            self.exit_queue.enqueue(job, 0)
                            self.running_queue.remove(job)
                        else:
                            self.running_queue.remove(job)
                            self.enqueue_priority_queue(job)

                    if job.time_slice_remaining == 0:
                        for cpu in self.cpus:
                            if cpu.job and cpu.job.job_id == job.job_id:
                                cpu.free()
                        if job.priority < 5:
                            job.priority += 1
                            self.running_queue.remove(job)
                            self.enqueue_priority_queue(job)
                        else:
                            self.running_queue.remove(job)
                            self.enqueue_priority_queue(job)

    def process_io_queue(self, client_id, session_id):
        if not self.io_queue.is_empty():
            for job in self.io_queue.jobs:
                if job.burst_complete():
                    for io in ios:
                        if io.job and io.job.job_id == job.job_id:
                            io.free()
                    job.get_job_burst(client_id, session_id, job.job_id)
                    if job.burst_type == "IO":
                        self.waiting_queue.enqueue(job)
                        self.io_queue.remove(job)
                    elif job.burst_type == "EXIT":
                        self.exit_queue.enqueue(job, 0)
                        self.io_queue.remove(job)
                    else:
                        self.ready_queue.enqueue(job)
                        self.io_queue.remove(job)
                else:
                    job.decrement_duration()

    def is_done(self):
        """Returns True if all queues are empty."""
        return all(
            queue.is_empty()
            for queue in [
                self.new_queue,
                self.ready_queue,
                self.running_queue,
                self.waiting_queue,
                self.io_queue,
                self.exit_queue,
            ]
        )

    def run(self, filters):
        """Runs the scheduler."""
        client_id = filters["client_id"]
        session_id = filters["session_id"]
        clock_time = filters["clock_time"]
        time_quantum = filters["time_quantum"]
        sched = filters["sched"]
        preemptive = filters["preemptive"]
        priority = False

        if sched == "PR":
            priority = True

        with Live(self.generate_table("MLFQ"), refresh_per_second=20) as live:
            while True:
                self.clock.increment()
                clock_time = self.clock.get_time()
                self.fetch_jobs(client_id, session_id, clock_time)
                self.move_to_ready_queue(client_id, session_id, algorithm=sched)
                self.process_ready_queue(algorithm=sched, priority=priority)
                self.process_running_queue(
                    client_id,
                    session_id,
                    algorithm=sched,
                    preemptive=preemptive,
                    time_quantum=time_quantum,
                )
                self.process_waiting_queue()
                self.process_io_queue(client_id, session_id)
                live.update(self.generate_table(algorithm=sched))
                sleep(0.5)


def api_start(configFile, seed=None):
    with open(configFile) as f:
        config = json.load(f)

    if seed is not None:
        config["seed"] = seed

    response = init(config)
    session_id = response["session_id"]
    start_clock = response["start_clock"]
    time_quantum = response["time_slice"]

    return start_clock, session_id, time_quantum


if __name__ == "__main__":
    kwargs, args = myKwargs(sys.argv)
    sched = kwargs["sched"]
    seed = kwargs["seed"]
    n_cpus = kwargs["cpus"]
    n_ios = kwargs["ios"]
    config = kwargs["config"]
    
    if "preemptive" in kwargs:
        preemptive = kwargs["preemptive"]
    else:
        preemptive = False

    start_clock, session_id, time_quantum = api_start(config, seed)

    cpus = [Device(f"CPU{i+1}") for i in range(n_cpus)]

    ios = [Device(f"IO{i+1}") for i in range(n_ios)]

    system_clock = SystemClock(start_clock)
    scheduler = Scheduler(system_clock, cpus, ios)
    clock_time = system_clock.get_time()
    filters = {
        "client_id": "serwes",
        "session_id": session_id,
        "time_quantum": time_quantum,
        "clock_time": clock_time,
        "sched": sched,
        "seed": seed,
        "preemptive": preemptive,
    }
    scheduler.run(filters)
    stats = Stats()
    stats.calculate_stats(scheduler.exit_queue)
    stats.print_stats()
