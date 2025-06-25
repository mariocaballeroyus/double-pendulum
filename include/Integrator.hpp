#pragma once

#include "DoublePendulum.hpp"

class Integrator
{
public:
    Integrator(const double timeStep)
        : timeStep_(timeStep) {}

    void stepRK4(DoublePendulum& system);

    const double getTimeStep() const { return timeStep_; }
private:
    const double timeStep_;
};