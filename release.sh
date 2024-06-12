#bin/bash
git add .
git commit -m "Release"
git push origin main
# Remove all tags from the repository
git fetch
# Delete all tags
git tag -l | xargs git tag -d
# Create tag read 'version' from che.properties file
version=$(grep "version" che/che.properties | cut -d'=' -f2)
git tag -a "$version" -m "Release $version"
git push origin "$version"
# Create a pre-release on GitHub
gh release create "$version" -t "$version" -n "Release $version" --prerelease
