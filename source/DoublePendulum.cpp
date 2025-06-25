#include "DoublePendulum.hpp"

Vec4 DoublePendulum::computeRHS(const Vec4& state) const
{
    // Unpack the state vector
    const double theta1 = state(0);
    const double omega1 = state(1);
    const double theta2 = state(2);
    const double omega2 = state(3);

    // Constants
    const double m1 = mass_[0];
    const double m2 = mass_[1];
    const double l1 = length_[0];
    const double l2 = length_[1];
    const double g = gravity_;

    // Construct the left-hand side matrix
    Mat2 lhs;
    lhs(0, 0) = (m1 + m2) * l1;
    lhs(0, 1) = m2 * l2 * cos(theta1 - theta2);
    lhs(1, 0) = l1 * cos(theta1 - theta2);
    lhs(1, 1) = l2;

    // Construct the right-hand side vector
    Vec2 rhs;
    rhs(0) = - m2 * l2 * omega2 * omega2 * std::sin(theta1 - theta2) - (m1 + m2) * g * std::sin(theta1);
    rhs(1) = l1 * omega1 * omega1 * std::sin(theta1 - theta2) - g * std::sin(theta2);

    // Solve the system for the angular accelerations
    Vec2 alpha = lhs.inverse() * rhs;

    // Construct the RHS of the ODE
    Vec4 sol;
    sol << omega1, alpha(0), omega2, alpha(1);
    
    return sol;
}