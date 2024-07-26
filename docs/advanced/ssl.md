If you want to deploy EZAuth you may want to run it via `HTTPS` instead of `HTTP`. This can be easily achieved with EZAuth, by putting certificates in the `config/ssl` directory. The certificates have to be named **`cert.pem` and `key.pem`**. The `cert.pem` file should contain the certificate and the intermediate certificate, while the `key.pem` file should contain the private key.

EZAuth will automatically detect the certificates and run on `HTTPS` instead of `HTTP`. If you want to run EZAuth on `HTTP` again, just remove the certificates from the `config/ssl` directory.

## Self Signing with [MKCert](https://github.com/FiloSottile/mkcert)

If you want to test EZAuth with self-signed certificates, you can use [MKCert](https://github.com/FiloSottile/mkcert).

!!! warning "SSL Certificates"
    Make sure that the certificates are valid and not self-signed. Browsers will not accept self-signed certificates and will show a warning to the user. Use [Let's Encrypt](https://letsencrypt.org/) or a similar service to get valid certificates.

To generate a self-signed certificate with MKCert, [install MKCert](https://github.com/FiloSottile/mkcert?tab=readme-ov-file#installation) and follow the instructions below.

=== "Debian/Ubuntu"
    Run the following commands to generate a Certificate with MKCert

    ```bash
    cd config
    mkdir -p ssl
    cd ssl
    mkcert yourdomain.com localhost 127.0.0.1
    ```

=== "Windows"
    Create a new folder in the `config` directory called `ssl`. Open a command prompt and navigate to the `config/ssl` directory. Run the following command to generate a Certificate with MKCert

    ```sh
    mkcert yourdomain.com localhost 127.0.0.1
    ```

After running the command, you will see two files in the `config/ssl` directory: `yourdomain.com.pem` and `yourdomain.com-key.pem`. Rename the files to `cert.pem` and `key.pem` respectively. Then restart the EZAuth service to apply the changes.