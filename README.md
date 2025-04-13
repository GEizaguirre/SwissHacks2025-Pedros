# Enabling Open Data in StartupTicker

**Team Members:**  
Pedro’s team – German Eizaguirre, Miquel Álvarez, Enrique Molina  
Participating in the **INNOSUISSE & STARTUPTICKER Challenge**

### 📚 Abstract
An fully scalable, out-of-the-box dashboard for start-up analytics. We focus on the reality of public organizations --a limited/non-extensible pool of resources-- and deliver a practical solution to run analytics in the client with minimal management burden. For that, we leverage WebAssembly, a programming language for the web that (1) runs in any browser --with light device requirements-- and (2) runs fast, as it is compiled just-in-time. The resulting system is a usable interface, easy to deploy, fully-fledged and, specially, requiring almost no adaptations of the backend


Pedro's is a group of three PhD students from Universitat  i Virgili (Tarragona, Spain). Our expertise centers on Cloud and distributed systems, but we are passionate on prototyping and delivering open-source solutions to the general public. We are determined to contribute to the Swiss small-to medium scale business ecosystem and transfer our experience from academic to industrial domains.


### 🌐 Project Overview
This project delivers a **public web application** that aims to **democratize access to startup data**, offering a platform that is:
- Transparent  
- Graphical  
- Simple  
- Reactive  
- Reliable  
- Customizable  

The interface is designed to be convenient and realistic, avoiding complexity traps. It supports both **simplified common queries** and **fully custom queries directly from the browser**, **reachable from any device** and **avoiding the need for a local installation**.

### 🛠️ Technical Implementation
- **SQL database(s)**: we maintain the current organization setup. 
- **REST proxy** for querying: just deploy the proxy and connect to the database.
- **Data plotting and visualization** occurs all the client side, using the novel yet powerful capabilities of Miramo, WASM and Pyoride.

### 💡 Key Strengths
- Lightweight solution that avoids prohibitive AI overhead (in the context of this business requirements)
- Very close to be a potential final dashboard.  
- Negligible operational cost
- Already live and functional: [cloudlab.urv.cat/swisshacks](http://cloudlab.urv.cat/swisshacks)  
- Designed for non-expert users, at the same time this is a powerful tool that is giving full control to the user.
- Perfect fit to StartupTicker’s requirements

### 🧭 Mission & Vision
The solution is **tailored to StartupTicker’s specific needs**, emphasizing **perfect fit and flexibility**.  
We believe in the long-term potential of this project and hope it will evolve far beyond its current state 🚀

### 🤔 Don't you believe us?
Check it out yourself! ;). Don't hesisate to visit the website and play with it [cloudlab.urv.cat/swisshacks](http://cloudlab.urv.cat/swisshacks) .