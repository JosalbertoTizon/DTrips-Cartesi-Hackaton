# dTrips

  

**dTrips** is a decentralized application built using Cartesi, designed to facilitate ride-sharing in a decentralized environment. This dApp leverages blockchain technology to ensure transparency, security, and a trustless environment for both drivers and passengers.

  

## Table of Contents

  
- [Installation](#installation)

- [Running a Local Cartesi Node](#running-a-local-cartesi-node)

- [Usage](#usage)

- [Contributing](#contributing)

- [License](#license)

  

  

## Installation

  

### Setup Python Virtual Environment

  

1.  **Clone the repository:**

  

```bash

git clone https://github.com/yourusername/dTrips.git

cd dTrips

```

  

2.  **Create a virtual environment:**

  

```bash

python3 -m venv venv

```

  

3.  **Activate the virtual environment:**

  

- On Linux/Mac:

  

```bash

source venv/bin/activate

```

  

- On Windows:

  

```bash

.\venv\Scripts\activate

```

  

4.  **Install Python dependencies:**

  

```bash

pip install -r requirements.txt

```

## Running a Local Cartesi Node

To use the dDrive app, you'll need to run a local Cartesi node. Follow these steps to get started:

1. **Install Cartesi CLI and Dependencies**  
   First, you'll need to install the Cartesi CLI and its dependencies. For detailed instructions, please refer to the official Cartesi documentation: [Cartesi CLI Installation Guide](https://docs.cartesi.io/cartesi-rollups/1.3/development/installation/).

2. **Running the Local Node**  
   Once you have the Cartesi CLI installed, navigate to the `dapp` folder inside your project directory:

   ```bash
   cd project_path/dapp
   cartesi build
   cartesi run


The dapp should now be hosted on http://localhost:8545. You can now interact with the dTrips application.
  
## Transactions

Transactions on the dTrips app are made using our token called **RideCoin**. These transactions are securely stored on Cartesi servers, which provide a scalable and efficient solution for managing the application's transactional data.

## Usage
Watch this video for a step-by-step demonstration of how to use dTrips:
[DTrips Demonstration](https://drive.google.com/drive/folders/1hM5tVrO3pD0q420y1p64MgkWEciSIMkR?usp=sharing)

  



  

## Contributing

  

We welcome contributions! Please fork the repository and submit a pull request for any enhancements, bug fixes, or new features.

  

## License

  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.