# Traffic-Engineering-Projects

This reporitory is for the three projects developed in the course of Traffic Engineering in ULisboa - Instituto Superior Tecnico 2025/2026

## Report Notes:

We use `u = random.random()` to generate random uniform numbers between `[0,1)`

The delta-t is the interval of time between two events

Common mistakes when using the hist() function (this is where most people lose points):
- Making histogram of dt instead of arrivals
- Using non-unit intervals
- Using round() instead of int() (breaks binning)
- Forgetting that Poisson is about counts per time, not time gaps

What a Poisson distribution looks like:

**What we expect theoretically**

For a Poisson distribution with **λ = 5**:
```
P(X=k)= (λ^k)x(e^−λ)/k!
```

### Key properties:
- Mean ≈ λ = 5
- Peak usually around k = 4 or 5
- Right-skewed (longer tail to the right)

### Next step (for your report)
You’ll need to:
- Repeat for λ = {0.5, 1, 5, 10, 50}
- Comment:

Typical observations:
- Small λ → skewed (many zeros)
- Large λ → looks almost Gaussian

Mention:

“A virtual environment was used to manage dependencies such as Matplotlib, ensuring reproducibility and avoiding conflicts with system-managed Python packages.”

**You should observe:**

- The combined process behaves like a Poisson with λ = sum
- As N increases → better match with theory
- For large λ (like 37):
    - Distribution becomes more symmetric
    - Approaches a Gaussian shape

### M/M/1 Queuing

### What your loop is really doing

Your loop is not “running one process”.

It’s doing this:
- Jump to next event in time
- Process it instantly
- Jump to next event
- Repeat

So time goes like:
```
t = 0.0  → arrival
t = 0.3  → arrival
t = 0.5  → departure
t = 0.7  → arrival
...
```

👉 You are **simulating a system evolving over time** — not executing tasks in parallel.

### Why this works (and is standard)

This is called Discrete Event Simulation (DES).

It is used in:
- network simulators
- operating systems research
- telecom systems
- traffic systems

And almost always:
👉 **single-threaded**

### How “concurrency” actually appears

Let’s say:
- A packet arrives at t = 1.0
- Another arrives at t = 1.1
- Service takes 2 seconds

Even without threads:
- First packet starts service
- Second packet waits in queue

Your simulation captures this because:
- the server is marked busy
- the queue stores waiting packets

#### Testing (initial state)

🔹 Case 1: Stable system
```
LAMBDA = 2
MU = 3
```

👉 Expect:
- queue stays small
- server sometimes idle

🔹 Case 2: Overloaded system
```
LAMBDA = 5
MU = 3
```

👉 Expect:
- queue grows continuously
- server always busy

### What metrics should you add?

For an M/M/1, the most important ones are:

1. Average waiting time (Wq)

Time a packet spends in the queue

2. Average system time (W)

Time in queue + service

3. Average queue length (Lq)
4. Server utilization (ρ̂)

Fraction of time server is busy