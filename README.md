# WorkSauce

Showcase and archive of the top-ranked web developer portfolios as indexed by Google

## Setup 

1. Download [phantomjs](http://phantomjs.org/download.html)
2. Create a Python virtual environment 
    
    > python -m venv venv/

3. Activate the virtual environment

    > source venv/bin/activate

4. Install the requirements

    > pip install -r requirements.txt

5. Run the build script
    
    > python build.py


### Other Commands

These don't need to be run manually, but are here for reference.

```bash
webscreenshot -i data/20230110-domains.txt -r phantomjs -o screenshots/20230110 --crop "0,0,1280,720" -f "jpg" -v
```

