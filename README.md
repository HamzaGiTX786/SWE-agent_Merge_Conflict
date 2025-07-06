# SWE-agent_Merge_Conflict

This is a test repo to evaluate the effectiveness of SWE-agent in resolve merge conflicts. 

## 📝 Information

- The repo contains files that have been changed in `branch a` in directory `a`, and files changed in `branch b` in directory `b`. 
- The `base` directory contains files prior to any changes in `branch a` or `branch b`. 
- `merged` contains the files after `branch a` and `branch b` have been merged. 
- The diffs (`<<<<` & `>>>>`) represent a merge conflicts, and show the code that needs a resolution

## 🔴 Issues

- To evaluate SWE-agent, the merge conflict is represented as an issue
- The SWE-agents is tasked with resolving the merge conflict using the issue description

## 🙏 Acknowledgement

- [Congra benchmark dataset](https://github.com/HKU-System-Security-Lab/ConGra)