# Verifying the papers

`SHA256SUMS` lists the SHA-256 digests of the three PDFs. `SHA256SUMS.asc` is its detached OpenPGP signature by the
author's key (`VincentLiu-signing-key.asc`), `SHA256SUMS.tsr` an RFC 3161 timestamp token over it and
`SHA256SUMS.ots` an OpenTimestamps proof anchored in Bitcoin. The same files are in the Zenodo record of each paper.

```
sha256sum -c SHA256SUMS
gpg --import VincentLiu-signing-key.asc
gpg --verify SHA256SUMS.asc SHA256SUMS
ots verify SHA256SUMS.ots
```
