#pragma once

#include <Eigen/Dense>

using Vec4 = Eigen::Vector4d;
using Vec2 = Eigen::Vector2d;
using Mat2 = Eigen::Matrix2d;

class DoublePendulum
{
public:
    DoublePendulum(double mass1, double mass2, double length1, double length2, double gravity)
    : mass_{mass1, mass2}, length_{length1, length2}, gravity_{gravity}, state_(Vec4::Zero()) {}

    void updateState(const Vec4& newState) { state_ = newState; }
    Vec4 computeRHS(const Vec4& state) const;

    Vec4 getState() const { return state_; }
    const std::array<const double, 2>& getMass() const { return mass_; }
    const std::array<const double, 2>& getLength() const { return length_; }
    const double getGravity() const { return gravity_; }
private:
    std::array<const double, 2> mass_;
    std::array<const double, 2> length_;
    const double gravity_;
    Vec4 state_;
};