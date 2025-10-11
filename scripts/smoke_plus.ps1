$ErrorActionPreference = "Continue"
$BASE = "http://127.0.0.1:8000"

function Show {
    param(
        [string]$label,
        $code,
        $expect = $null
    )
    $ok = $true
    if ($expect -ne $null) { $ok = ($code -eq $expect) }
    if ($ok) {
        Write-Host ("[{0}] {1}" -f $code, $label) -ForegroundColor Green
    } else {
        Write-Host ("[{0}] {1}" -f $code, $label) -ForegroundColor Yellow
    }
}


$r = Invoke-WebRequest -Uri "$BASE/healthz" -Method GET -ErrorAction SilentlyContinue
if ($r) { $code = $r.StatusCode } else { $code = "ERR" }
Show "GET /healthz" $code 200


$rand = Get-Random
$email = "me+$rand@example.com"
$pwd = "Passw0rd!"
$registerBody = @{ email=$email; password=$pwd; full_name="Gaal Jaylaani" } | ConvertTo-Json
$r = Invoke-WebRequest -Uri "$BASE/auth/register" -Method POST -ContentType "application/json" -Body $registerBody -ErrorAction SilentlyContinue
if ($r) { $code = $r.StatusCode } else { $code = "ERR" }
if ($code -eq 201) { $expected = 201 } else { $expected = 200 }
Show "POST /auth/register ($email)" $code $expected

$loginBody = @{ email=$email; password=$pwd } | ConvertTo-Json
$login = Invoke-RestMethod -Uri "$BASE/auth/login" -Method POST -ContentType "application/json" -Body $loginBody -ErrorAction SilentlyContinue
if (-not $login -or -not $login.access_token) {
    Write-Host "Login failed" -ForegroundColor Red
    exit 1
}
Show "POST /auth/login" 200 200
$TOKEN = $login.access_token
$authHeader = @{ Authorization = "Bearer $TOKEN" }

$me = Invoke-RestMethod -Uri "$BASE/users/me" -Method GET -Headers $authHeader -ErrorAction SilentlyContinue
if (-not $me) {
    Write-Host "GET /users/me failed" -ForegroundColor Yellow
} else {
    if ($me.email -ne $email) {
        Write-Host "users/me email mismatch" -ForegroundColor Yellow
    }
}
Show "GET /users/me" 200 200

$createBody = @{
    name="Barbell Row"
    muscle_group="Back"
    equipment="Barbell"
    instructions="Hinge at hips, pull to torso, control down."
} | ConvertTo-Json
$ex = Invoke-RestMethod -Uri "$BASE/exercises" -Method POST -Headers $authHeader -ContentType "application/json" -Body $createBody -ErrorAction SilentlyContinue
if (-not $ex -or -not $ex.id) {
    Write-Host "POST /exercises failed (no id)" -ForegroundColor Red
    exit 1
}
$EX_ID = $ex.id
Show "POST /exercises" 201 201


$r = Invoke-WebRequest -Uri "$BASE/exercises" -Method GET -Headers $authHeader -ErrorAction SilentlyContinue
if ($r) { $code = $r.StatusCode } else { $code = "ERR" }
Show "GET /exercises" $code 200


$one = Invoke-RestMethod -Uri "$BASE/exercises/$EX_ID" -Method GET -Headers $authHeader -ErrorAction SilentlyContinue
if (-not $one -or $one.id -ne $EX_ID) {
    Write-Host "GET /exercises/{id} mismatch" -ForegroundColor Yellow
}
Show "GET /exercises/{id}" 200 200

$updateBody = @{
    name="Barbell Bent-Over Row"
    muscle_group="Back"
    equipment="Barbell"
    instructions="Flat back, pull to lower ribs."
} | ConvertTo-Json
$upd = Invoke-RestMethod -Uri "$BASE/exercises/$EX_ID" -Method PUT -Headers $authHeader -ContentType "application/json" -Body $updateBody -ErrorAction SilentlyContinue
if (-not $upd -or $upd.name -ne "Barbell Bent-Over Row") {
    Write-Host "PUT /exercises/{id} not updated" -ForegroundColor Yellow
}
Show "PUT /exercises/{id}" 200 200

$del = Invoke-WebRequest -Uri "$BASE/exercises/$EX_ID" -Method DELETE -Headers $authHeader -ErrorAction SilentlyContinue
if ($del) { $code = $del.StatusCode } else { $code = "ERR" }
if ($code -eq 204) { $expected = 204 } else { $expected = 200 }
Show "DELETE /exercises/{id}" $code $expected

try {
    $check = Invoke-WebRequest -Uri "$BASE/exercises/$EX_ID" -Method GET -Headers $authHeader -ErrorAction Stop
    $code = $check.StatusCode
} catch {
    if ($_.Exception.Response) {
        $code = $_.Exception.Response.StatusCode.Value__
    } else {
        $code = "ERR"
    }
}
Show "GET /exercises/{id} after delete - expect 404" $code 404

Write-Host ""
Write-Host "Smoke+ checks done." -ForegroundColor Cyan
