# Project Review Notes

Repository: `cloud-native-monitoring-eks`

## What I cleaned or improved

- Rebuilt the main README with a career-progression story.
- Added your requested animated footer/contact section.
- Added screenshot references. Existing snapshots were copied into `docs/screenshots` when available.
- Kept `.env`, secrets, Terraform state, kubeconfigs, and token files blocked in `.gitignore`.
- Added cleanup/cost-control commands in README.
- Added Kubernetes manifests under `k8s/` for cleaner EKS deployment explanation.
- Kept this repo without active GitHub Actions workflows to avoid automatic failed runs before AWS setup.

## Review before making public

- Run the validation commands in README on your laptop.
- Replace any placeholder registry, bucket, cluster, domain, and account values with your own lab values.
- Add your own latest screenshots if this repo does not already include screenshots.
- Do not commit real cloud credentials, tokens, kubeconfigs, private keys, `.env`, or Terraform state.
