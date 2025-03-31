# Top Level Domains (TLDs)

This folder contains a curated list of known malicious or suspicious **Top-level domains (TLDs)** sourced from various reputable threat intelligence and security organizations.

These TLDs are commonly associated with malicious activities such as **phishing**, **malware distribution**, **spam**, and other types of cyber threats.

## Introduction

Top-level domains (TLDs) are the final segment of a domain name, appearing after the last dot (e.g., .com, .org, .xyz). 

Certain TLDs are frequently abused by malicious actors due to their permissive registration policies, low costs, or lack of proper oversight.

The list is updated periodically based on new data and reports from various sources.

## Sources

The list of malicious TLDs has been sourced from the following trusted threat intelligence providers:

- [Spamhaus](https://www.spamtitan.com/)
- [SpamTitan](https://www.spamtitan.com/)
- [Interisle](https://interisle.net/)
- [DomainTools](https://whois.domaintools.com/)
- [Unit42](https://unit42.paloaltonetworks.com/)
- [WhoisXML](https://www.whoisxmlapi.com/)
- [Symantec](https://sep.securitycloud.symantec.com/v2/landing) 

### Malware Reports

- [Cybercrime Supply Chain 2024](https://static1.squarespace.com/static/63dbf2b9075aa2535887e365/t/673a102318cc943de2987231/1731858468631/CybercrimeSupplyChain2024.pdf)

- [Interisle](https://interisle.net/insights/phishing-landscape-2024-an-annual-study-of-the-scope-and-distribution-of-phishing)

- [WhoisXML](https://main.whoisxmlapi.com/blog/december-2022-new-domain-activity-highlights/pdf)

- [A Peek into Top-Level Domains and Cybercrime](https://unit42.paloaltonetworks.com/top-level-domains-cybercrime/)

### Articles

- [DomainTools names and shames bad TLDs](https://domainnamewire.com/2022/07/15/domaintools-names-and-shames-bad-tlds/)

- [Bad .Men at .Work. Please Don't .Click](https://krebsonsecurity.com/2018/06/bad-men-at-work-please-dont-click/#more-44137)

- [The "Top 20": Shady Top-Level Domains](https://www.security.com/feature-stories/top-20-shady-top-level-domains)

- [NextDNS - Spamhaus Most Abused TLDs List](https://help.nextdns.io/t/h7hg88p/spamhaus-most-abused-tlds-list)

- [SpamHaus Project](https://www.spamhaus.org/reputation-statistics/cctlds/domains/)
   
## File Format

The TLDs are stored in text format, with one TLD per line, formatted as a regex to be used for [Pihole](https://pi-hole.net/).

Below is an example format:

```
(^|\.)cam$
(^|\.)club$
```

## Making use

This list of malicious TLDs can be used for a variety of cybersecurity applications, such as:

- Blocking or filtering access to known malicious TLDs.
- Integrating the TLD list into threat detection systems or firewalls.
- Enriching domain reputation checks or security monitoring systems.
- Enhancing phishing detection and mitigation strategies.

To integrate the list into your system, you can download the file and parse the TLDs for further use in any way you like.

## License

This repository is licensed under the MIT License. Use it freely for personal, educational, and professional purposes, but please credit the sources and contributors.
