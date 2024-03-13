## Langkah menjalankan test pertama dengan Docker Container

$ docker build -t damvfastapitest . 
$ docker run -d --name damvfastapitest-svc -p 5005:5005 damvfastapitest

# Test di postmen
# - memasukkan data
curl --location --request POST 'http://localhost:5005/api' \
--form 'nama="admin"' \
--form 'umur="23"'

# - mendapatkan data
curl --location --request GET 'http://localhost:5005/api'

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
❯ flyctl apps create --name damvflaskapitest
Update available 0.0.456 -> v0.0.457.
Run "flyctl version update" to upgrade.
automatically selected personal organization: abumuhammad
New app created: damvflaskapitest


❯ flyctl deploy
Update available 0.0.456 -> v0.0.457.
Run "flyctl version update" to upgrade.
==> Verifying app config
--> Verified app config
==> Building image
Remote builder fly-builder-bitter-field-1943 ready
==> Creating build context
. . .
--> Pushing image done
image: registry.fly.io/damvflaskapitest:deployment-01GSAG095HEJETPHNP7W4YFSAQ
image size: 915 MB
==> Creating release
--> release v2 created

--> You can detach the terminal anytime without stopping the deployment
==> Monitoring deployment
Logs: https://fly.io/apps/damvflaskapitest/monitoring

 1 desired, 1 placed, 1 healthy, 0 unhealthy [health checks: 1 total, 1 passing]
--> v0 deployed successfully

❯ flyctl open
Update available 0.0.456 -> v0.0.457.
Run "flyctl version update" to upgrade.
opening http://damvflaskapitest.fly.dev ...


# Test di postmen
# - memasukkan data
curl --location --request POST 'http://damvflaskapitest.fly.dev/api' \
--form 'nama="admin"' \
--form 'umur="23"'

# - mendapatkan data
curl --location --request GET 'http://damvflaskapitest.fly.dev/api'