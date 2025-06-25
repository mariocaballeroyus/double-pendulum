#pragma once

#include "DoublePendulum.hpp"
#include "Integrator.hpp"

class Simulation
{
public:
    Simulation(DoublePendulum& system, Integrator& integrator, const double timeEnd)
    : system_(system), integrator_(integrator), timeEnd_(timeEnd) {}

    void run();

    const std::vector<Vec4>& getTrajectory() const { return trajectory_; }
    const DoublePendulum& getSystem() const { return system_; }
private:
    DoublePendulum& system_;
    Integrator& integrator_;
    const double timeEnd_;
    std::vector<Vec4> trajectory_;
};