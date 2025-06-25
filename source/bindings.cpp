#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include "Integrator.hpp"
#include "DoublePendulum.hpp"
#include "Simulation.hpp"

namespace py = pybind11;

PYBIND11_MODULE(doublePendulum, m) {
    py::class_<DoublePendulum>(m, "DoublePendulum")
        .def(py::init<double, double, double, double, double>(),
             py::arg("mass1"), py::arg("mass2"), py::arg("length1"), py::arg("length2"), py::arg("gravity"))
        .def("updateState", &DoublePendulum::updateState, py::arg("newState"));

    py::class_<Integrator>(m, "Integrator")
        .def(py::init<double>(), py::arg("timeStep"));

    py::class_<Simulation>(m, "Simulation")
        .def(py::init<DoublePendulum&, Integrator&, double>(),
             py::arg("system"), py::arg("integrator"), py::arg("timeEnd"))
        .def("run", &Simulation::run)
        .def("getTrajectory", &Simulation::getTrajectory);
}