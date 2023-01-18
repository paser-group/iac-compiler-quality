## Quality Assurance for Infrastructure Orchestrators 

## Background 

Infrastructure as code (IaC) is the practice of automatically managing computing infrastructure at scale. IaC is implemented using infrastructure orchestrators, i.e., tools that implement the practice of IaC, such as Ansible. Use of infrastructure orchestrators have yielded several benefits for organizations. 

A tool of such importance needs systematic integration of quality assurance activities, such as testing and fuzzing. However, IaC is na emerging field, and researchers in general have overlooked this domain. This means opportunities for us, as we can do a series of research studies in this domain. 

## Overall Objective 

As the first step towards this goal we aim to conduct a research study as part of which we will develop a fuzzing technique that will expose latent bugs in infrastructure orchestrators. If everything goes into plan, then we can expect the research findings to be submitted top tier conference and journal papers. The nature of the project will give us flexibility to submit the paper at top-tier NLP, AI, software engineering, or security venues. Once successful, me and Dr. Karmaker will submit 1/2 grant proposals based on this work, which in turn will help support Smith as a RA, and seamlessly finish his PhD work without being a TA.    

I have listed the following papers that use NLP or ML to conduct compiler fuzzing, which Smith can take motivation from. It shows that compiler fuzzing has appeal to a wide range of top-tier venues. Depending on the story and analysis we can pick one.  

- USENIX Security: [Montage](https://www.usenix.org/system/files/sec20summer_lee-suyoung_prepub_0.pdf) 
- ESEC/FSE: [Deep learning compilers](https://haoyang9804.github.io/A_Comprehensive_Study_of_Deep_Learning_Compiler_Bugs.pdf)
- AAAI: [DeepFuzz](https://ojs.aaai.org/index.php/AAAI/article/view/3895) 
- ISSTA: [DeepSmith](https://chriscummins.cc/pub/2018-issta.pdf) 
- ICSE: [Neuzz](http://lingming.cs.illinois.edu/publications/icse2022e.pdf)
- ASPLOS: [NNSmith](http://lingming.cs.illinois.edu/publications/asplos2023.pdf) 
- ASE: [RecBi](https://lingming.cs.illinois.edu/publications/ase2020b.pdf) 

While writing the paper, we need to `skilfully distance` ourselves from [Lingming](https://lingming.cs.illinois.edu/) so that the reviewers do not question the novelty work. But, that's for future.  

## Steps  

- Install Ansible. [Link](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#), [source](https://github.com/ansible/ansible) 
- Create a simple Ansible manifest to copy a file from your computer to an [EC2 Instance](https://aws.amazon.com/ec2/). Tutorial: [URL](https://medium.datadriveninvestor.com/devops-using-ansible-to-provision-aws-ec2-instances-3d70a1cb155f). My [manifest](sample.yml). My [hosts file](akond-hosts). Command to run my manifest: 
```
ansible -i hosts all -m ping
ansible-playbook -vvv -i akond-hosts sample.yml 
``` 

- Once the above two steps are done, you can confirm that you hae installed Ansible successfully, and you are also able to create a Ansible manifest successfully. Your next step is to use NLP to generate the same manifest without causing any errors. Once you are able to do that, then we can start the experimentation process, where we can tweak your code generation process to generate Ansible manifests that will expose latent bugs in the Ansible compiler. 

- You can also leverage existing manifests used for test cases. They are available in  [invalid](invalid/). I would recommend that you use your own mutated manifest to try fuzzing first.  

## Lessons Learned 

- Sequence to sequence encoding didn’t perform well 