pollutionCommute_Sever
===

This is a small flask webservice developed as part of my final year project. It facilitated the ingest and displaying of PM pollution, along with an auth system that allows a user to create an account. This account the allows the user to add sensors to the account, this makes use of The Things Network API to create a new device in the application simplifying the process of getting DevEUI and app keys.

## install

```bash
git clone https://github.com/ioangogo/pollutionCommute_Sever.git
cd pollutionCommute_Sever
python3 -m venv venv
source bin/activate
pip install -r requirements.txt
```
edit the `commutePolluteServer.yaml`, rename `config.cfg.example` to `config.cfg.example` and edit the replace mes, and add the path of the venv to the `commutepollute.ini` file

copy `commutePolluteServer.yaml` to where you systemd services are, reload the daemon and start the service