<div id="top"></div>

<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]

</div>

</br>

<div align="center">
  <a href="https://github.com/LovroG05/UniKlaud">
    <img src="images/logo.png" alt="Logo" width="180" height="180">
  </a>

  <h1 align="center">UniKlaud</h1>

  <h3 align="center">
    Run your clouds in RAID
  </h3>

  </br>
</div>

<div align="center">

  ![][linux-shield]
  ![][windows-shield]
  ![][macos-shield]

</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The goal of this project is to be able to join multiple online storages from different or same providers and create one big storage space with a simulated filesystem

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python 3](https://www.python.org/)
* [PyDrive2](https://pypi.org/project/PyDrive2/)
* [Dropbox](https://pypi.org/project/dropbox/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The install instructions for the released version will be released with the version, but here are the instructions for cloning

### Installation

1. Install the requirements
    ```sh
    pip3 install -r requirements.txt
    ```
3. Get your client_secrects.json from [Google Cloud](https://cloud.google.com/) using [this guide](https://medium.com/analytics-vidhya/how-to-connect-google-drive-to-python-using-pydrive-9681b2a14f20) and copy it to the root of the project
4. Get your dropbox API key and secret using [this guide](https://www.dropbox.com/developers/documentation/python#tutorial). Rename ```sample_dotenv``` to ```.env``` and replace the respectable values in it. Remember to enable all permissions under individual scopes.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

_Please refer to the [Wiki](https://github.com/LovroG05/UniKlaud/wiki)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- Release 1:
    - Google Drive and Dropbox
    - A simple CLI
- Redesign the interface
- GUI using PyQt5 most likely

See the [open issues](https://github.com/LovroG05/UniKlaud/issues) and [TODOs](https://github.com/LovroG05/UniKlaud/projects/1) for a full list of proposed features, todos and known issues.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU-3.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact
LovroG05 - [@LovroG05](https://twitter.com/LovroG05)

chocoearly44 - [@chocoearly44](https://twitter.com/chocoearly44)

<p align="right">(<a href="#top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/LovroG05/UniKlaud.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/LovroG05/UniKlaud.svg?style=for-the-badge
[forks-url]: https://github.com/LovroG05/UniKlaud/network/members
[stars-shield]: https://img.shields.io/github/stars/LovroG05/UniKlaud.svg?style=for-the-badge
[stars-url]: https://github.com/LovroG05/UniKlaud/stargazers
[issues-shield]: https://img.shields.io/github/issues/LovroG05/UniKlaud.svg?style=for-the-badge
[issues-url]: https://github.com/LovroG05/UniKlaud/issues
[license-shield]: https://img.shields.io/github/license/LovroG05/UniKlaud.svg?style=for-the-badge
[license-url]: https://github.com/LovroG05/UniKlaud/blob/master/LICENSE

[windows-shield]: https://img.shields.io/badge/Windows-Not%20yet-red?style=for-the-badge&logo=windows
[linux-shield]: https://img.shields.io/badge/Linux-Yes-green?style=for-the-badge&logo=linux
[macos-shield]: https://img.shields.io/badge/MacOs-Untested-orange?style=for-the-badge&logo=apple