# Double Pendulum System

## Installation

1. Clone the project

```bash
git clone -r https://github.com/mariocaballeroyus/double-pendulum.git
```

2. Build the C++ extension

```bash
mkdir build
cd build
cmake ..
make
```

3. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Run the simulation

```bash
python3 run.py
```

## Project overview

This project simulated the dynamics of a planar double pendulum. The main objective is to explore and compare different time integration methods for nonlinear ODEs with a particular focus on **energy conservation** properties.

Currently, the simulation uses an explicit RK4 method. In the future, it will be extended to include a symplectic energy-preserving integrator, allowing for a deeper investigation into the long-term behavior of the system.

## Formulation

We consider a planar double pendulum composed of two point masses $` m_1, m_2 `$, two massless rigid rods of lengths $` L_1, L_2 `$ and gravity $` g `$ acting downward.

### Kinematics

We define the **positions** of the two masses with respect to a fixed origin located at the top of the pivot:

```math
\begin{align*}
x_1 &= L_1 \sin(\theta_1)
, &\quad 
x_2 &= x_1 + L_2 \sin(\theta_2) 
\\
y_1 &= -L_1 \cos(\theta_1)
, &\quad 
y_2 &= y_1 - L_2 \cos(\theta_2)
\end{align*}
```

Taking the time derivatives of the positions, gives us the **velocities** of the two masses:

```math
\begin{align*}
\dot{x}_1 &= L_1 \cos(\theta_1) \, \dot{\theta}_1
, &\quad
\dot{x}_2 &= \dot{x}_1 + L_2 \cos(\theta_2) \, \dot{\theta}_2 
\\
\dot{y}_1 &= L_1 \sin(\theta_1) \, \dot{\theta}_1
, &\quad
\dot{y}_2 &= \dot{y}_1 + L_2 \sin(\theta_2) \, \dot{\theta}_2
\end{align*}
```

For energy calculations:

```math
\begin{align*}
v_1^2 &= \dot{x}_1^2 + \dot{y}_1^2 = L_1^2 \dot{\theta}_1^2
\\
v_2^2 &= \dot{x}_2^2 + \dot{y}_2^2 = L_1^2 \dot{\theta}_1^2 + L_2^2 \dot{\theta}_2^2 + 2L_1L_2\dot{\theta}_1\dot{\theta}_2\cos(\theta_1 - \theta_2)
\end{align*}
```

### Energy

The vertical height of each mass determines its **gravitational potential energy**:

```math
\begin{align*}
V &= m_1 g y_1 + m_2 g y_2 \\
  &= -(m_1 + m_2) g L_1 \cos\theta_1 - m_2 g L_2 \cos\theta_2
\end{align*}
```

Each mass also has a **kinetic energy** associated with its velocity:

```math
\begin{align*}
T &= \tfrac{1}{2} m_1 v_1^2 + \tfrac{1}{2} m_2 v_2^2
\\
  &= \tfrac{1}{2}(m_1 + m_2)L_1^2 \dot{\theta}_1^2
+ \tfrac{1}{2} m_2 L_2^2 \dot{\theta}_2^2
+ m_2 L_1 L_2 \dot{\theta}_1 \dot{\theta}_2 \cos(\theta_1 - \theta_2)
\end{align*}
```

### Equations of Motion

To derive the Equations of Motion, we define the **Lagrangian**:

```math
\mathcal{L} = T - V
```

From this, we apply the **Euler-Lagrange Equations** for $` \theta_1 `$ and $` \theta_2 `$:

```math
\frac{d}{dt} \left( \frac{\partial \mathcal{L}}{\partial \dot{\theta}_i} \right) - \frac{\partial \mathcal{L}}{\partial \theta_i} = 0
```

This gives us two coupled second-order nonlinear ODEs. Defining $` M = m_1 + m_2 `$ and $` \Delta = \theta_1 - \theta_2 `$, we get:

```math
\begin{aligned}
M L_1 \ddot{\theta}_1 
+ m_2 L_2 \ddot{\theta}_2 \cos\Delta
+ m_2 L_2 \dot{\theta}_2^2 \sin\Delta 
+ M g \sin\theta_1 &= 0 \\
L_2 \ddot{\theta}_2 
+ L_1 \ddot{\theta}_1 \cos\Delta
- L_1 \dot{\theta}_1^2 \sin\Delta 
+ g \sin\theta_2 &= 0
\end{aligned}
```

## Numerical solution

### State Vector and Initial Conditions

Since most numerical integration schemes are designed to operate on first-order systems, we must first transform ours into a system of **first-order equations**. 

To achieve this, we introduce the angular velocity variables $` \dot{\theta}_1, \dot{\theta}_2 `$. With this substitution, our system is reformulated in terms of first-order variables. We group these into a single **state vector**:

```math
\mathbf{y} =
\begin{bmatrix}
\theta_1 & \dot{\theta}_1 & \theta_2 & \dot{\theta}_2
\end{bmatrix}^T
```

The values of this state vector at time $` t = 0 `$ constitute the **initial conditions** of the Initial Value Problem (IVP).

### Computing RHS

To evaluate the right-hand side $` \mathbf{f} `$, we also need the angular accelerations $` \ddot{\theta}_1, \ddot{\theta}_2 `$. These are obtained by solving the following linear system at each step:

```math
\begin{bmatrix}
M L_1 & m_2 L_2 \cos\Delta \\
L_1 \cos\Delta & L_2
\end{bmatrix}
\begin{bmatrix}
\ddot{\theta}_1 \\
\ddot{\theta}_2
\end{bmatrix}
=
\begin{bmatrix}
- m_2 L_2 \dot{\theta}_2^2 \sin\Delta - M g \sin\theta_1 \\
L_1 \dot{\theta}_1^2 \sin\Delta - g \sin\theta_2
\end{bmatrix}
```

Now, the time evolution of our system can be written compactly as:

```math
\frac{d \mathbf{y}}{dt} = \mathbf{f}(\mathbf{y}) = 
\begin{bmatrix}
\dot{\theta}_1 & \ddot{\theta}_1 & \dot{\theta}_2 & \ddot{\theta}_2
\end{bmatrix}^T
```

### Time Integration

To numerically integrate this system, we use a classical **explicit fourth-order Runge-Kutta** method (RK4). The scheme advances the solution from $` \mathbf{y}^{n} `$ to $` \mathbf{y}^{n+1} `$ using multiple intermediate evaluations of $` \mathbf{f} `$:

```math
\mathbf{y}^{n+1} = \mathbf{y}^n + \frac{1}{6}(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4)
```

The intermediate values are defined as follows:

```math
\begin{align*}
\mathbf{k}_1 &= \Delta t \cdot \mathbf{f}(\mathbf{y}^n) 
&\quad 
\mathbf{k}_3 &= \Delta t \cdot \mathbf{f}\left(\mathbf{y}^n + \tfrac{1}{2} \mathbf{k}_2\right) \\
\mathbf{k}_2 &= \Delta t \cdot \mathbf{f}\left(\mathbf{y}^n + \tfrac{1}{2} \mathbf{k}_1\right) 
&\quad 
\mathbf{k}_4 &= \Delta t \cdot \mathbf{f}\left(\mathbf{y}^n + \mathbf{k}_3\right)
\end{align*}
```