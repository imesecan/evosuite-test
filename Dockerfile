# Container image for running EvoSuite
# FROM openjdk:18-jdk
FROM ubuntu:latest

WORKDIR /evosuite
RUN apt update
RUN apt install less nano zip unzip
RUN apt install default-jre default-jdk -y
COPY copy-files /evosuite/
