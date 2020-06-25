# Sync IHE documents locally
# allows windows to exec ps1 shell
# Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
# https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-6

Param(
    [String[]]$domains
    )

$domains_list=[string]::Join(",",$domains)

if  ($domains) {
	write-output "Sync domains : $domains_list"
	docker run -ti --rm -v ${PWD}:/opt/data flrt/ihe-tf-sync python ihesync/sync.py --domain $domains_list
} else {
    write-output "Sync all domains"
	docker run -ti --rm -v ${PWD}:/opt/data flrt/ihe-tf-sync python ihesync/sync.py
}
