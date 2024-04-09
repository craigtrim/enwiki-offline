# enwiki-offline


# DVC (Data Version Control)

## Initialize DVC and Configure S3 Remote
In your project root, initialize DVC if you haven't already, and configure your S3 bucket as the remote storage. Replace `enwikioffline` with your actual S3 bucket name if it's different. Run:

```shell
dvc init
dvc remote add -d myremote s3://enwikioffline
dvc remote modify myremote profile enwiki_offline
```

This setup:
- Initializes DVC in your project.
- Adds your S3 bucket as the default remote storage.
- Configures DVC to use the `enwiki_offline` AWS profile for S3 operations.

## Track and Push Data with DVC
To track the resources folder and push it to S3, execute:
```shell
dvc add resources
git add resources.dvc .gitignore
git commit -m "Track resources folder with DVC"
dvc push
```

This process:
- Tracks the `resources` folder with DVC, creating a .dvc file.
- Commits the DVC files to Git.
- Pushes the data to your S3 bucket using the configured AWS profile.

## Pull Data with DVC
To retrieve the data managed by DVC, use:
```sh
dvc pull
```
This command pulls the data from S3 into your local `resources` folder, based on the current DVC setup and the latest `resources.dvc` file in your repository.
