---
title: DNP3 TLS test certificates
description: 
layout: page
visibility: public
version: 
tags:
- networking
- security
---
 
### 📜 Change Log
 **Date**   | **Name**      | **Change**         | **Version** |
 |------------|---------------|---------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-13 |  | created document | 2.0.2606 |
 





# DNP3 TLS test certificates

Examples CA chain for mutual TLS between an AnyLog DNP3 **Master Station** and an **outstation** (for example [opendnp3](https://github.com/dnp3/opendnp3) `outstation-demo` configured for TLS).

## Generate

```bash
cd "05- Networking & Security/C- DNP3 certificates/ca_chain"
bash create_certificates.sh
```

## Files

| File | Role |
|------|------|
| `anylogDNP3ca.cert` / `anylogDNP3ca.key` | Root CA |
| `master1.cert` / `master1.key` | TLS certificates to start the AnyLog Master Station |
| `outstation1.cert` / `outstation1.key` | TLS certificates to start the primary test outstation |
| `outstation2.cert` / `outstation2.key` | TLS certificates to start a second outstation (optional) |

## Certificates and keys (collapsed)

Click to expand each PEM. **For testing only** — do not reuse these keys in production.

### Certificates

<details>
<summary>anylogDNP3ca.cert — Root CA</summary>

```pem
-----BEGIN CERTIFICATE-----
MIIDdzCCAl+gAwIBAgIUT0s0cDdDXj4j32nv1RjPUzb4gw0wDQYJKoZIhvcNAQEL
BQAwSzELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk9SMQ0wCwYDVQQHDARCZW5kMSAw
HgYDVQQKDBdBbnlMb2cgQ2VydGlmaWNhdGUgQ29ycDAeFw0yNjA3MTQxNDE2NTda
Fw0zNjA1MjIxNDE2NTdaMEsxCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJPUjENMAsG
A1UEBwwEQmVuZDEgMB4GA1UECgwXQW55TG9nIENlcnRpZmljYXRlIENvcnAwggEi
MA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCG1958/jEZhWMXjBK6Jb1yZOYI
rhO9s8Kua1VTi/pQ/CveDnwX8UdVaa+iH4Zcfoq5s49EMN2eZMaeUxlizRgPgKuA
D+DQpNZWdgOonPYbM8/2bmoQiC2y2YiBnS8zuXhje+cKHsBYi70tYR5CarS85qvF
vsHANBLKDo0LhhYYuVeVYe9bInxxJLsCN9E74zlkc6IEk0AIFEvqsP6mKad9SwgJ
gLFo0TF2NJ+QdCHANGi0WO4mmv+2LM6uJhcmOqWZYo9AHl0JAIiFX88jCtgF1DzU
iTc2dtqVf05Zp8Olre+QOIgPNNfSTjULnj0X5BAU7xiqwJvNXrx7ra5q+EttAgMB
AAGjUzBRMB0GA1UdDgQWBBTR+2sBy/iPr3cPIIeaKj8utfX+JTAfBgNVHSMEGDAW
gBTR+2sBy/iPr3cPIIeaKj8utfX+JTAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3
DQEBCwUAA4IBAQBP7jJoEF9DSQpyn3P/oiJtOdrdaRi1PNc3VG0npsVARjaKZ0GT
BR5Ij2a+ZaDkevvk8nZhMUWgGZTM4xShqDQqLJOxn/vAOzEghTM1d5NMCUWO++sp
UwAbunAuuIPQ5ANVUS0+s3tZTkL54UCz8vAZ7QiRR4pLHcqR1UWPR41fNPczNGNB
RcLDYY5t7Ru76OggnoHVyozyqP0BP2fgW45lxe1ohCug5AVBwTtcH7x081feV7GT
5r1nfTUCLzxEn+rkULBxOVcazRFzbJZxC0CuV3I2JJbjyJPFklQakzxSQNKSCznW
rSbfgqyRjelhtwonTHc4F+33VaOciVfT7yCc
-----END CERTIFICATE-----
```

</details>

<details>
<summary>master1.cert — TLS certificate to start the AnyLog Master Station</summary>

```pem
-----BEGIN CERTIFICATE-----
MIIDXDCCAkSgAwIBAgIUGATy7wU9sEWgFNQ2WfAkYkEtcw8wDQYJKoZIhvcNAQEL
BQAwSzELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk9SMQ0wCwYDVQQHDARCZW5kMSAw
HgYDVQQKDBdBbnlMb2cgQ2VydGlmaWNhdGUgQ29ycDAeFw0yNjA3MTQxNDE2NTda
Fw0zNjA1MjIxNDE2NTdaMEExCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJPUjETMBEG
A1UECgwKQW55TG9nRE5QMzEQMA4GA1UEAwwHbWFzdGVyMTCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAKNVaGcwemTaxI2sxM0ZakuSrYVGk8EzvPl1yYk9
oD/7I3cRJtXROTUyzZwqemg390hi6UQteTkFMXyKD+7MZVoAOdNFcWWcVLUHApcu
BORMlLdOuQ4pYhhvcBDnSrNVMsp67Bu30/TlpYIGHtDVIdyxuF3zqjixR923nEOi
OIkvpo8iqKdkLYxsYUaLf+FFebCjz5x9cwwr3iWoKt3vE+h21RQL+TwVzEI0MZ8n
EOtJo7DiiU0dQIoNhBtCeynSWpMgYn6e7u2ES3xeuXRWAPNP93eCoFVamGkLz2vL
hZecXdeWw1Gwlbq942fMqBiZHDc23l2Vhl9H891PfwEEITUCAwEAAaNCMEAwHQYD
VR0OBBYEFO4KbfdT4ZKTf75Wx0inDarbHuu4MB8GA1UdIwQYMBaAFNH7awHL+I+v
dw8gh5oqPy619f4lMA0GCSqGSIb3DQEBCwUAA4IBAQCEmjChmVaBniW/mupTG9uJ
NswnaGbmio1CXNZaKlv4Om3nz7JE5C0U949GhS3RLus8CbFAnAxjVheXcJdspsyo
dk0U3c15XsNo1Ob+tigvcU/BDsIWKExxggr6IC5oRfUoNAi9MIX86KrxRyeic8zz
Kf3B9tjRzzntORCilaOGNQWJnIXGnZ/Y9h8gkMjJxzZXPWojSMbRN5pMjVb0yakz
9xkg1v2aKdNz/DZN55ilG8isyDfghAvlav56D6ECfubL1PUfP8vNCY4gnHvjdYST
BwXlJAfNG3OWQ4UOvsAihfXMNHnIDlxuvPaaomZhqJHi/M9EbO2f2rTGfQMfoUT5
-----END CERTIFICATE-----
```

</details>

<details>
<summary>outstation1.cert — TLS certificate to start the primary outstation</summary>

```pem
-----BEGIN CERTIFICATE-----
MIIDYDCCAkigAwIBAgIUGATy7wU9sEWgFNQ2WfAkYkEtcxAwDQYJKoZIhvcNAQEL
BQAwSzELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk9SMQ0wCwYDVQQHDARCZW5kMSAw
HgYDVQQKDBdBbnlMb2cgQ2VydGlmaWNhdGUgQ29ycDAeFw0yNjA3MTQxNDE2NTda
Fw0zNjA1MjIxNDE2NTdaMEUxCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJPUjETMBEG
A1UECgwKQW55TG9nRE5QMzEUMBIGA1UEAwwLb3V0c3RhdGlvbjEwggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQCb846OncGJFdLxZJ1pUtzSeXMYW/L9xUho
3wp7LMQUWDnsbZBlP3nd7uoMaev36T/cB66vjYRxcNys4NzDVq8WdaxLzDrwD+Dh
RyES6xY2PuFLFiosrJNFz6QSZG0YeOR3Ass+8Ri10OqOElvIcnJPyS8VteGDAOwk
xgdKWPNEo/zQC7YFP9wcsdOKF3aODbAleGgmdMy/sM6fGk6Dv8M4RJ6y+ng2D7V3
qkVukAwHPRzEmLnjAhyrzazVKn917qXHQFExzpJ2U9P33khw3p8CMXu3HbTUIG5J
RK+AGaAIWZSkezZzrah8EOiRySkpmC1mW6bszEVrOGJr+iMDn/sbAgMBAAGjQjBA
MB0GA1UdDgQWBBQlttY3UKFlAidRFzAlnXM9pTTLFTAfBgNVHSMEGDAWgBTR+2sB
y/iPr3cPIIeaKj8utfX+JTANBgkqhkiG9w0BAQsFAAOCAQEAgixXfVFybhehLK1X
ZLSvLtJMPEyRJ/GUT+tss/bxP3r+54A3kSp/6BseYlIRVung01easC6YdxUpGFKq
TrCaiiFOQp4oWVNl+XduNS2GZ/1CocIxvehlih+IPxu1RKhhBQn3HPQRYq5TEFgT
orMQN+YRvIDZeqpWdzUNFGf+tu3eyUOj9CQbLex5oTVTDGacTwGj1Ox4Rm2D9dPx
iHZnDNRfs7b1jrhhfUBqtzYnuMd8rpuLk1sQAPVKW/mopBibssxtxYPITTP0Aney
HoqtWg0cFJ8xnAJmD0UM1xVFx9b1J11jOEfdlxcUnR1YF8aXdYmF96KnZx61cIaX
reSnWw==
-----END CERTIFICATE-----
```

</details>

<details>
<summary>outstation2.cert — TLS certificate to start a second outstation (optional)</summary>

```pem
-----BEGIN CERTIFICATE-----
MIIDYDCCAkigAwIBAgIUGATy7wU9sEWgFNQ2WfAkYkEtcxEwDQYJKoZIhvcNAQEL
BQAwSzELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk9SMQ0wCwYDVQQHDARCZW5kMSAw
HgYDVQQKDBdBbnlMb2cgQ2VydGlmaWNhdGUgQ29ycDAeFw0yNjA3MTQxNDE2NTda
Fw0zNjA1MjIxNDE2NTdaMEUxCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJPUjETMBEG
A1UECgwKQW55TG9nRE5QMzEUMBIGA1UEAwwLb3V0c3RhdGlvbjIwggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQCU8yf7UM4Y8zaGlJRArYrZoMn6A1M98LQj
4L7Azi8YG3ox6bIi/tOoE4woKyrR5iiafkYosJ/9njaCCDOKbxV6ly3ojZqmVoNQ
qZksEDjvkdxb12rIaMHa1+L5Qlp9uhQueOl+m+FlcksHprKrrcgPxA9qC2ov8OJi
uswAp+xxJ2Txw2/1lRxINxTskEFDPLAzI8De3vO5O3sUN33EpJxRsHmryhpatwSf
Ba1XzDJBD82/48wW9lOwZeP38RZju+5eMXxLecKGVnQeIYsPwgl/3tga1dgz/1cs
thJClPkBLB+dGP89XbH4IzTcIpJ38WEYWPB77bKiMtPofG0RZzDdAgMBAAGjQjBA
MB0GA1UdDgQWBBTTsz2SsFjmYObB7IzwvMCqjgWIMjAfBgNVHSMEGDAWgBTR+2sB
y/iPr3cPIIeaKj8utfX+JTANBgkqhkiG9w0BAQsFAAOCAQEAIl8bxUuXRJEEUrur
KfZFxuihWUsQZdwPdxQx7H53bcqGn66Cv7YX5dYeIMzOuTP4/efTC8dJYETA2554
hBz5Z9pAA/WGtnPTRzbngi0BtcheB94TkzEfp6Uhmobq0yzNLeVVvZsNWmBfwpO9
wa+JeRRxs4Z6gmCmdwskcaC8atIttdoNJ05IE3W5+OJrdK50pJPK70m9boeXqwb6
6mKRtiUCbppbDVQATIXhHakThycMg6dDtj+1LBO1q571r8IrOa/guke3SKDU6qrq
/EJ6EL1+SojRLk7R/oZwF6yA9rkW5tnjUGL45YMBz+9SWxrwZcW/UmLrQL+L9LID
i1vkdw==
-----END CERTIFICATE-----
```

</details>

### Private keys

<details>
<summary>anylogDNP3ca.key — Root CA private key</summary>

```pem
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCG1958/jEZhWMX
jBK6Jb1yZOYIrhO9s8Kua1VTi/pQ/CveDnwX8UdVaa+iH4Zcfoq5s49EMN2eZMae
UxlizRgPgKuAD+DQpNZWdgOonPYbM8/2bmoQiC2y2YiBnS8zuXhje+cKHsBYi70t
YR5CarS85qvFvsHANBLKDo0LhhYYuVeVYe9bInxxJLsCN9E74zlkc6IEk0AIFEvq
sP6mKad9SwgJgLFo0TF2NJ+QdCHANGi0WO4mmv+2LM6uJhcmOqWZYo9AHl0JAIiF
X88jCtgF1DzUiTc2dtqVf05Zp8Olre+QOIgPNNfSTjULnj0X5BAU7xiqwJvNXrx7
ra5q+EttAgMBAAECggEADPpOwAHo8NddI6GIFeFW++EJILG8Vags5wOOiUVyGIRE
ppEHUXiX0Hkk/boCAPnu2ROWiM4ZLkrtsMQ3r8IkfC16lA8zKHGM7XJbRMmiiBiy
/bk/vQqWN13nXO4nYleJ5i1BHcC662q7kNgFhQfnED01MAl9dUWtv0OqQH8ttkBQ
kA8i/6FGw7tRinnxnNmLIXNbzg2usyvLoGClRrR7MN7EmMQisp3wwL0b650ecPMc
VMOUfJshzOrEfMe8OTdfrPzlrEnpzpxR9x2xNZ/Y0SYIUMAUf0+Q2TQUp9TYDISJ
Whx2hlGkMszhdNTwyk81Ndl/ppeH4uChz+DQ9IPzMQKBgQC9RUW9H45qzTi0PioP
ZxVOJjDn5dt+4jQ5sxt+n0BuQO/tXkbKSkQ6j3iwMXfur4J2Yt75HTfq5toXbd4G
sZ9tBDXDv/Ukl9GRY0/cLsFGbJ/SsD3QSEWxFeRl6cHArYLFlxvO+cA8yjVp1sW4
GmyuoENLi6wUViVrPtD+2wK35QKBgQC2YjlVxpi9mv1TVz3edATvUoi6glaPQK7T
2UpOo6AxNKVmOCyNIOtamFOPZRy1BU72+HQKqWpKCYWDirVSwXP/mtBFb38oofag
yaNTegSYHN+xCPvnNXWlQaHanvVrSFgO2vGNudMR+RjNvAYNfjUFUmMhhH+tvhuP
RiGB0/x86QKBgBuQ4ERYOTzS4ORXfXa6076LD2pm7t3/Ag45SNLbTN4B9S/EIFlM
Eb3ZsYEv40DPLRgi9Eih+cfrkW4CIWkmK4sMJux4o7KNrgcXyMTPxnSEU46y/n28
WPIetyIktoRigP5YMMOnWllANiFRF4Dl0FhqnQJ+uDRKC68f+f50VWQFAoGBAI6v
ebupi4WK4/V3o2eNzO6O23lOzvlz2VLUBFZRnNniHiRCflhLENXnpjfhGvxkEssU
xXQx5n3VxSaMNh9wSZgHPjmUaR8Y1yIjniuIol9+92JBbRINuOR43G91PPuZtYqp
r6D5aC//eXA7UWDtA/4N3pAyYNFEkbsdWsl/V2FBAoGAGTbDmfcGtMTjMrS+mlho
/vXgfYJXqXTSNndZAGeqCj6w2Yby1wm2viwT8Mxa/jXNiofuEsRgEIkFBeFxE6kn
A8azJ6+z9OLjc69b0jhqlx9P5UxePigfEyTqsR4kAyI03HizGHySOaC+K7eL80jD
Mwsj2tSGIajCktegmwU0t1s=
-----END PRIVATE KEY-----
```

</details>

<details>
<summary>master1.key — Private key to start the AnyLog Master Station</summary>

```pem
-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCjVWhnMHpk2sSN
rMTNGWpLkq2FRpPBM7z5dcmJPaA/+yN3ESbV0Tk1Ms2cKnpoN/dIYulELXk5BTF8
ig/uzGVaADnTRXFlnFS1BwKXLgTkTJS3TrkOKWIYb3AQ50qzVTLKeuwbt9P05aWC
Bh7Q1SHcsbhd86o4sUfdt5xDojiJL6aPIqinZC2MbGFGi3/hRXmwo8+cfXMMK94l
qCrd7xPodtUUC/k8FcxCNDGfJxDrSaOw4olNHUCKDYQbQnsp0lqTIGJ+nu7thEt8
Xrl0VgDzT/d3gqBVWphpC89ry4WXnF3XlsNRsJW6veNnzKgYmRw3Nt5dlYZfR/Pd
T38BBCE1AgMBAAECggEAFREC1m2xbkkB2UzDf2P79UO1tL8TIfQEjN+tKac0quaU
lEVhOb/IE1Kk+V5Ii8uizd0laAvoxZAkFK47+tlgaHjR/IF0QZ5Qa0mRrc0biBSm
iR69Yz8MLh76wyYJ2P0wAAoAYlzV7jwhGkGkKjGV3Kthc7YQqkpB/NizQ3fstyjP
hS9Q1fgJZDGvsrsqhPlvdUWni4Be5eHRejqY85HgTcceV8cY8+TW92dYFgJIZJt4
tWhhu4AHPn/QapyxlhkI1MVLJECfUVhD8HdI42vCtRehQ2v3dqFgIfofd1lBJ0fC
t+RLeOpIvkVDrSnxbsnGrN0KGKLgAvOzRXngTmwKiwKBgQDaCUUDmkGPzDQNN3rj
c8eXm/bLbW2bxKf74Phx4/kstip1hEe6ZDCbXPzVM9z6hFwUDf4tuE9Q+DmO0U8N
MrS6uUr7vsDuUKawKBHkhFnAhf0dRZ9smxpc3e/AkgCP2XXc4xB7Oc6iIgwIkWtW
qG8tD3X6oi1Z+XjS6rslVRWqPwKBgQC/xdRBavlqr+3UK3yxcRT7BRH7/KDuxLMa
gJwFc+0iWZI2qKnJ+y3qjz71PsX9Qhbqrw8ggziCRIgzdm1akY3TM4AwrZJaBGPH
ack9Ya2tM93SmL2qmd1/jziAyAid086qRoCjL7MZjYoOVJEkMHjA/E1Yhgd8pRhB
wb1EjvkPiwKBgQDBv+z495F888vpVry39AGP4sMbIEF/YvCXbeG4awnYRoRSa1rF
8hQTaz0tQ+oBH68nDwwompi47etP0wV5R+674r4UGP0eiMKm1OSZeVa8MxSqd1zk
yKtTjNBpAhTHv0jyIUBbEBJjlve0gWyt0/z/QLbpIkZEpuBMJNRqp0IaRwKBgQCj
IyCQUfdBWc4A6smVjTQi4kpNSbiBxdTy26tePCLjUL1AQDTH/SQvYJJXQIJfEoS6
OhetOdOtha0z0i/ultnGbA5F2rIgX5GeBxDJZbnAGNpAF+1pHqE9rVGMxB4IXTF2
yqkNqTs7pptl22zpE072JOuLPeFKmItNDQn8M4AORwKBgQCLNPlk5mUwLI5Kc1yF
J5X2zCvn7YTY+Ax9IOsaaAjnjC2ggxcvSQ0AgnCXwqDmDsc9R1kGFTFNloCq3Xqq
2M5uODzcPBjQtKts1w8uhKJU1di2quUcjJtoLA/sac1zcuyypfIOPHv8zY5uKC4b
tU+GK+95LbPZHmzjY6I2pxorYg==
-----END PRIVATE KEY-----
```

</details>

<details>
<summary>outstation1.key — Private key to start the primary outstation</summary>

```pem
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCb846OncGJFdLx
ZJ1pUtzSeXMYW/L9xUho3wp7LMQUWDnsbZBlP3nd7uoMaev36T/cB66vjYRxcNys
4NzDVq8WdaxLzDrwD+DhRyES6xY2PuFLFiosrJNFz6QSZG0YeOR3Ass+8Ri10OqO
ElvIcnJPyS8VteGDAOwkxgdKWPNEo/zQC7YFP9wcsdOKF3aODbAleGgmdMy/sM6f
Gk6Dv8M4RJ6y+ng2D7V3qkVukAwHPRzEmLnjAhyrzazVKn917qXHQFExzpJ2U9P3
3khw3p8CMXu3HbTUIG5JRK+AGaAIWZSkezZzrah8EOiRySkpmC1mW6bszEVrOGJr
+iMDn/sbAgMBAAECggEAB/ghP8519mBkICvJE3nFiQflxsfkGe277of/TB4Ugwmj
JB7RMytUOfAci7fZ9Bg6SC8oURZFP1rKHBd9kIncdqRawqDUHjJhhoGRAht7ThhW
gPTIAPJssDOVKc9x978txZsh8bx2S8w6QDpV8F9Q0hzwyAY8WOpyJsrr0nPLMqWu
MbiR6UB98jZSu3FtG9gWeY6TeuAQ3lCruNQ5HmONfp7tcwNGeYpJ2lEWuAZhEv4e
hupM3uTyfRPDi8NFHtTXSKNqdflXThi/3J8ilJ4HCmSe8OD8BHVFv96RGBfN0WNp
F2F7cLOv0mipzbaXX5ouGF9QFn5uXX4p3QMD8qfdKQKBgQDSfbZdqrL/HqGjbMsX
IecslZlOKsIPzUJ4v0vJnpE5FUAyOYAo8h16JECAKsl5J366aeNr9+8MRwgnaQ3j
LqKDPFR2zMnRdAXog3LT4qRh/L9Hhx2WBSgeTM4w8EG4t3ixbSGbgxwqrzkHHv5Q
bEtQS//1ynuW2wWBnxmTcSVV5wKBgQC9qyzvpL5OJbcjhQQrpsP1Gof0zGqFbAHJ
aheZt37Pr0D1nR7F1s6Uj/Vs0GtLwXVX9KxM/HDASCnXGOHCkUuDvRbhs/86l73o
mRyNkhRZk/UfDTnDu9Zu7w/CxeUO5cR9y5nn0zSTbPMTy0fSEwZBbWsFdoNfc/Oi
aUjArBnirQKBgFOl2Z8HgvKXfaywQ1UCCBhTqwTBQTV+YHgTrU6GUTfaFhTffOrI
rKYpWeiVGFOpOldiVRpHARxj7f2bZgVuNu7oPrinUVyHOwHXmv5RBvpZsrn+G+fO
TM8dvqL8F2IMp037DGv8gmkEESmfS3kyUAus6B8JRGwCxgFo9IT/ZdLpAoGBAJQx
mOytZdwdb9ia58VLibSKxEurJFeXKlY7RLFgQ/71yeWenBqsWcCOMo6Q0iTgxVSx
4aZNX7N9LuPXlx209LG8HpK/Vt5rDYEdkMe0qZ3MEyvt44Jh04vd0gy3Ht/i+wHn
ARu3VE8UQ2Dl5fnnz21zlrkv/jmomWX+qU+RqLAJAoGATd5gURj56SJ2zaBXv0Sa
mK0Ky+DCRszeeB9Fv43jmrU4cqM2v4pRQ3svODXs8Fiu7QKi6Ii4K1XToWgiVwU7
K49CoTteFptDRNwt60dd4N/fpOGGif6FsOzI9TShNlNddxkOE9eWeKbRuwU41e5l
P8MFxxhcLDE8qk+A7qb2qBw=
-----END PRIVATE KEY-----
```

</details>

<details>
<summary>outstation2.key — Private key to start a second outstation</summary>

```pem
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCU8yf7UM4Y8zaG
lJRArYrZoMn6A1M98LQj4L7Azi8YG3ox6bIi/tOoE4woKyrR5iiafkYosJ/9njaC
CDOKbxV6ly3ojZqmVoNQqZksEDjvkdxb12rIaMHa1+L5Qlp9uhQueOl+m+FlcksH
prKrrcgPxA9qC2ov8OJiuswAp+xxJ2Txw2/1lRxINxTskEFDPLAzI8De3vO5O3sU
N33EpJxRsHmryhpatwSfBa1XzDJBD82/48wW9lOwZeP38RZju+5eMXxLecKGVnQe
IYsPwgl/3tga1dgz/1csthJClPkBLB+dGP89XbH4IzTcIpJ38WEYWPB77bKiMtPo
fG0RZzDdAgMBAAECggEAF43B/0xeYvSm5S4+qWGoCNUTy2zWL3/ORLQoBf401UeX
EaiGamFIoBYDPmDhIxMVzaR1PL79ddIchYB9ggEh8OJSOKmX0IDywAEpvx2Lm1rB
8WYFtU5XhV9JPahf/ey8f0LQjZxhzrR9p+aU73AKKHAVDexjLNSXQAyQ8POdAKF/
4ZISVWq/angBd+aw6PQYZUGZ9VfXYSTKXTu2e1gvJU81Xb+LRAP/S6eSzVRzHDmu
6HgeaWF+f2EfrU/ItbFrtUvYJrQHzmeq4yGxYN8kapBIufcNvG5kBut6d07j4uki
Xu7ys7JN1EZ3mHeObQF5ouAL33ZQE2RwoBlGS8MIMQKBgQDGL+SVWsjrXEcKcxCZ
tgU2lKsIDEK9dyhOrc2NMH0Wv6EC232gh6PL9MbjM3Tf2yLIp9W6+P5cZHsaCWuy
3aRknI57lGmEBOM2igEgOWPJrfuh5sDjXSQAv64gJeh9C0GHk9o3ndaJmmzRZgmE
JETFxIYP2NAiIRMleHNLngI7dQKBgQDAZlm5dGvCIKEOvO5vhhPiE0/+yu7MP99J
Wa2RmQqSN9odmmnSVKGI4ZsaNCs+E4ytsbnV8XhbqgqaitlgFBOGxkE1ZB8p+tY6
Fpaz916gBFx95SOy1fCOxqmTA6dz2dRhOHST2zuUvpYxSwOBjFS2lwJGT4s0Jo2e
GKRl77Y6yQKBgAbJNQZ4KVEFw9jzv6nDtcH8rS6FXPOn1NV81gDznBTfUuAKK+8H
NfCR3Q2CgYn4suQz+vl/9RWsyxpFIE7rj+lyAt7wYfyHPlBrwUYdMPGC547Pm+Mt
GUJ9TbUEF0XQ0NmXkm09Fk933in9WG4R39j1tbFtNxM0Fre9vBTmwCTRAoGBAKEi
VwzJ4yG/QAPe2XZPfUF+2SVUAfDPoYqF76ab3M2ety7JzsyXkn3YLJUikgC4UL57
tV7nj9x9KcpKdUlRJxVd3uj/RFZdPKODnY11pCsx2+CYUnCJWqHI4eY9TjXpfkQ6
CvB10I1/nLwFzhbmV2BgUkhegAAaNcrtamnw+9Z5AoGBAMNtu385jmVa+x31ScQn
mEJRc8CSjS7UHVbtrah4qjBWGJnIWt0kJD7UnLzoj+GngwTzESe2+/s06WkTAB/O
aT7n1tOfNr7+CZyejKLCUuFs6X0ll9u4rHTJ+kO3S7jGETrpqsrC5eZ6LIn+tL7f
ntBtAn9iu8aklpqjwdtHUDFt
-----END PRIVATE KEY-----
```

</details>

Verify the chain locally:

```bash
openssl verify -CAfile anylogDNP3ca.cert master1.cert outstation1.cert outstation2.cert
```

## AnyLog Master Station

Use paths relative to your working directory when running AnyLog, for example:

| Keyword | Path |
|---------|------|
| `tls_ca` | `/path/to/certs/anylogDNP3ca.cert` |
| `tls_cert` | `/path/to/certs/master1.cert` |
| `tls_key` | `/path/to/certs/master1.key` |

## TLS Outstation

Configure the outstation with:

| Setting | Path |
|---------|------|
| Peer / CA | `/path/to/certs/anylogDNP3ca.cert` |
| Local certificate | `/path/to/certs/outstation1.cert` |
| Private key | `/path/to/certs/outstation1.key` |

## TLS Outstation demo

After `bash create_certificates.sh`, from `~/opendnp3/build`:

```bash
./outstation-tls-demo \
  /path/to/certs/anylogDNP3ca.cert \
  /path/to/certs/outstation1.cert \
  /path/to/certs/outstation1.key
```

**For testing only** — do not reuse these keys in production.

See also: [DNP3](../../07-%20Southbound%20Interfaces/A-%20Direct%20-%20Built-in%20connectors%20%28protocols%20AnyLog%20natively%20accepts%20from%20devices%29/DNP3.md#dnp3-out-station-testing).
