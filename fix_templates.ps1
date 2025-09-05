$blogTemplatesDir = "d:\customyourspin\ads\templates\blog"
$files = Get-ChildItem -Path $blogTemplatesDir -Filter "*.html" | Where-Object { $_.Name -ne "base.html" -and $_.Name -ne "index.html" }

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Check if the file already has the load static tag
    if ($content -notmatch "{% load static %}") {
        # Replace the extends tag with extends tag + load static
        $newContent = $content -replace "{% extends `"blog/base.html`" %}", "{% extends `"blog/base.html`" %}$([Environment]::NewLine){% load static %}"
        
        # Write the modified content back to the file
        Set-Content -Path $file.FullName -Value $newContent
        
        Write-Host "Added {% load static %} to $($file.Name)"
    } else {
        Write-Host "$($file.Name) already has the load static tag"
    }
}

Write-Host "All templates have been updated!"