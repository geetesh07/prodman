<div align="center">
    <a href="https://prodman.com">
        <img src="https://raw.githubusercontent.com/frappe/prodman/develop/prodman/public/images/prodman-logo.png" height="128">
    </a>
    <h2>prodman</h2>
    <p align="center">
        <p>ERP made simple</p>
    </p>

[![CI](https://github.com/frappe/prodman/actions/workflows/server-tests.yml/badge.svg?branch=develop)](https://github.com/frappe/prodman/actions/workflows/server-tests.yml)
[![UI](https://github.com/prodman/prodman_ui_tests/actions/workflows/ui-tests.yml/badge.svg?branch=develop&event=schedule)](https://github.com/prodman/prodman_ui_tests/actions/workflows/ui-tests.yml)
[![Open Source Helpers](https://www.codetriage.com/frappe/prodman/badges/users.svg)](https://www.codetriage.com/frappe/prodman)
[![codecov](https://codecov.io/gh/frappe/prodman/branch/develop/graph/badge.svg?token=0TwvyUg3I5)](https://codecov.io/gh/frappe/prodman)
[![docker pulls](https://img.shields.io/docker/pulls/frappe/prodman-worker.svg)](https://hub.docker.com/r/frappe/prodman-worker)

[https://prodman.com](https://prodman.com)

</div>

prodman as a monolith includes the following areas for managing businesses:

1. [Accounting](https://prodman.com/open-source-accounting)
1. [Warehouse Management](https://prodman.com/distribution/warehouse-management-system)
1. [CRM](https://prodman.com/open-source-crm)
1. [Sales](https://prodman.com/open-source-sales-purchase)
1. [Purchase](https://prodman.com/open-source-sales-purchase)
1. [HRMS](https://prodman.com/open-source-hrms)
1. [Project Management](https://prodman.com/open-source-projects)
1. [Support](https://prodman.com/open-source-help-desk-software)
1. [Asset Management](https://prodman.com/open-source-asset-management-software)
1. [Quality Management](https://prodman.com/docs/user/manual/en/quality-management)
1. [Manufacturing](https://prodman.com/open-source-manufacturing-erp-software)
1. [Website Management](https://prodman.com/open-source-website-builder-software)
1. [Customize prodman](https://prodman.com/docs/user/manual/en/customize-prodman)
1. [And More](https://prodman.com/docs/user/manual/en/)

prodman is built on the [Frappe Framework](https://github.com/frappe/frappe), a full-stack web app framework built with Python & JavaScript.

## Installation

<div align="center" style="max-height: 40px;">
    <a href="https://frappecloud.com/prodman/signup">
        <img src=".github/try-on-f-cloud-button.svg" height="40">
    </a>
    <a href="https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/frappe/frappe_docker/main/pwd.yml">
      <img src="https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png" alt="Try in PWD" height="37"/>
    </a>
</div>

> Login for the PWD site: (username: Administrator, password: admin)

### Containerized Installation

Use docker to deploy prodman in production or for development of [Frappe](https://github.com/frappe/frappe) apps. See https://github.com/frappe/frappe_docker for more details.

### Manual Install

The Easy Way: our install script for bench will install all dependencies (e.g. MariaDB). See https://github.com/frappe/bench for more details.

New passwords will be created for the prodman "Administrator" user, the MariaDB root user, and the frappe user (the script displays the passwords and saves them to ~/frappe_passwords.txt).


## Learning and community

1. [Frappe School](https://school.frappe.io) - Learn Frappe Framework and prodman from the various courses by the maintainers or from the community.
2. [Official documentation](https://docs.prodman.com/) - Extensive documentation for prodman.
3. [Discussion Forum](https://discuss.prodman.com/) - Engage with community of prodman users and service providers.
4. [Telegram Group](https://prodman_public.t.me) - Get instant help from huge community of users.


## Contributing

1. [Issue Guidelines](https://github.com/frappe/prodman/wiki/Issue-Guidelines)
1. [Report Security Vulnerabilities](https://prodman.com/security)
1. [Pull Request Requirements](https://github.com/frappe/prodman/wiki/Contribution-Guidelines)
1. [Translations](https://translate.prodman.com)


## License

GNU/General Public License (see [license.txt](license.txt))

The prodman code is licensed as GNU General Public License (v3) and the Documentation is licensed as Creative Commons (CC-BY-SA-3.0) and the copyright is owned by Frappe Technologies Pvt Ltd (Frappe) and Contributors.

By contributing to prodman, you agree that your contributions will be licensed under its GNU General Public License (v3).

## Logo and Trademark Policy

Please read our [Logo and Trademark Policy](TRADEMARK_POLICY.md).
