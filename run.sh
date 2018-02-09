#!/usr/bin/env bash
gunicorn authenticationservice.app -b :80 --reload
