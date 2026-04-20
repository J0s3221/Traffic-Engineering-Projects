# Traffic-Engineering-Projects

This reporitory is for the three projects developed in the course of Traffic Engineering in ULisboa - Instituto Superior Tecnico 2025/2026

### Report Notes:

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

#### Key properties:
- Mean ≈ λ = 5
- Peak usually around k = 4 or 5
- Right-skewed (longer tail to the right)

#### Next step (for your report)
You’ll need to:
- Repeat for λ = {0.5, 1, 5, 10, 50}
- Comment:

Typical observations:
- Small λ → skewed (many zeros)
- Large λ → looks almost Gaussian

Mention:

“A virtual environment was used to manage dependencies such as Matplotlib, ensuring reproducibility and avoiding conflicts with system-managed Python packages.”