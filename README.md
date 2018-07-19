# TIMSE - Transparency in Multi-Service Environments
In multi-service environments service providers are handling personal data. By means of privacy policies they provide an overview about how personal data is handled. Because of the complexity of the policies the data handling is not transparent. By introducing the General Data Protection Regulation the EU mentioned transparency as key element. Data controllers should provide users insights in how their data is used, stored and processed. This work designs timse as tool enhancing transparency in multi-service environments to support service developers for a transparent representation of the intended data handling.

## Disclaimer
- **Please do not use this as an production system**, this is highly experimental.
- You should run this service at least using SSL and with an WSGI container such as [gunicorn](http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/#gunicorn).

## Quickstart
- `git clone https://github.com/PrivacyEngineering/timse`
- `cd timse/`
- `pip install -r requirements.txt`
- `sudo python timse.py`
- `curl http://localhost/x/status` should return `{
    "msg": "timse started successfully!"
}`
- Open [http://localhost/](http://localhost/) to access the API documentation
- Open [http://localhost/Dashboard](http://localhost/Dashboard) to explore the User Interface

## Live-Demo
- Dashboard: [http://timse-dashboard.implementation.cloud](http://timse-dashboard.implementation.cloud)
- API documentation: [http://timse-api.implementation.cloud](http://timse-api.implementation.cloud)
- Currently hosted at Google Cloud Platform

## Authors
This is joint work of Elias Grünewald, Saskia Nuñez von Voigt and Duc Linh Tran for the Research Group [Information Systems Engineering](https://www.ise.tu-berlin.de) at [TU Berlin](https://tu-berlin.de) as part of the course [Privacy Engineering](https://www.ise.tu-berlin.de/menue/lehre/module/privacy_engineering/) which is supervised by [Dr.-Ing. Frank Pallas](https://www.ise.tu-berlin.de/menue/team/dr_ing_frank_pallas/).
