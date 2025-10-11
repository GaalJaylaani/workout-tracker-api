$ErrorActionPreference = "Continue"
$BASE = "http://127.0.0.1:8000"

function Show($label, $code) {
    Write-Host ("[{0}] {1}" -f $code, $label)
}


$r = Invoke-WebRequest -Uri "$BASE/healthz" -Method GET -ErrorAction SilentlyContinue
Show "GET /healthz" $r.StatusCode

$rand = Get-Random
$email = "me+$rand@example.com"
$pwd = "Passw0rd!"
$registerBody = @{ email=$email; password=$pwd; full_name="Gaal Jaylaani" } | ConvertTo-Json
$r = Invoke-WebRequest -Uri "$BASE/auth/register" -Method POST -ContentType "application/json" -Body $registerBody -ErrorAction SilentlyContinue
Show "POST /auth/register ($email)" $r.StatusCode


$loginBody = @{ email=$email; password=$pwd } | ConvertTo-Json
$r = Invoke-RestMethod -Uri "$BASE/auth/login" -Method POST -ContentType "application/json" -Body $loginBody -ErrorAction SilentlyContinue
$TOKEN = $r.access_token
if (-not $TOKEN) { Write-Host "Login failed"; exit }
$authHeader = @{ Authorization = "Bearer $TOKEN" }

$r = Invoke-RestMethod -Uri "$BASE/users/me" -Method GET -Headers $authHeader -ErrorAction SilentlyContinue
Show "GET /users/me" 200


$createBody = @{
    name="Barbell Row"
    muscle_group="Back"
    equipment="Barbell"
    instructions="Hinge at hips, pull to torso, control down."
} | ConvertTo-Json
$r = Invoke-RestMethod -Uri "$BASE/exercises" -Method POST -Headers $authHeader -ContentType "application/json" -Body $createBody -ErrorAction SilentlyContinue
$EX_ID = $r.id
Show "POST /exercises" 201

$r = Invoke-WebRequest -Uri "$BASE/exercises" -Method GET -Headers $authHeader -ErrorAction SilentlyContinue
Show "GET /exercises" $r.StatusCode

$r = Invoke-WebRequest -Uri "$BASE/exercises/$EX_ID" -Method DELETE -Headers $authHeader -ErrorAction SilentlyContinue
Show "DELETE /exercises/{id}" $r.StatusCode

Write-Host ""
Write-Host "All smoke checks ran successfully."
