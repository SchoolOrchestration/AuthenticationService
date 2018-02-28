#!/usr/bin/env bash
py.test \
--cov=authenticationservice \
--cov-config .coveragerc \
authenticationservice/tests/

coverage xml
python-codacy-coverage -r coverage.xml