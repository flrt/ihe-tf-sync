# Sync IHE documents locally
Param(
    [String[]]$domains
    )

$domains_list=[string]::Join(",",$domains)

if  ($domains) {
	write-output "Sync domains : $domains_list"
	docker run -ti --rm -v ${PWD}:/opt/data flrt/ihe-tf-sync python sync.py --domain $domains_list
} else {
    write-output "Sync all domains"
	docker run -ti --rm -v ${PWD}:/opt/data flrt/ihe-tf-sync python sync.py 
}
