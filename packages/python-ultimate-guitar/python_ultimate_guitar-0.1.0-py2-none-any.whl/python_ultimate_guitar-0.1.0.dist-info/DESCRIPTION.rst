All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description: python-ultimate-guitar
        ==============
        
        python bindings for ultimate-guitar.com
        
        Supports:
        ----------
        - search with type filtering (pro, tab, chords, etc)
        - dowload tabs and guitar pro files
        
        
        Using from command line
        -----------------------------------
        ```bash
        ultimate-guitar search -q "paranoid android" -t guitar_pro --limit 10 --download 
        
        Usage: ultimate-guitar search [OPTIONS]
        
        Options:
          -q, --query TEXT            The person to greet.
          -t, --filter-type TEXT      Filter results by type
          -l, --limit INTEGER         Limit first N results
          -p, --path TEXT             Path to downloaded files
          --download / --no-download
          --help       
        
        ```
        
        
        
        Using as lib
        ----------------------------
        ```python
        from ultimate_guitar import UltimateGuitarScraper
        ug = UltimateGuitarScraper()
        ug.search('paranoid android')
        >>> <ResultSet: paranoid android returned 28 results>
        
        ug.search('paranoid android', filter_type='guitar_pro')
        <ResultSet: paranoid android returned 9 results>
        
        ```
        
        
Platform: UNKNOWN
