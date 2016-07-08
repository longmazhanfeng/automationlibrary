#robotframework-mobileLibrary
Here RobotFramework-WebLibrary is a updated library based on robotframework-selenium2library 1.7.4, 
we add some patches on it according to our project requirements


**Release notes**:
-----
###  1.0.1 @2016.2.24
> * Offer Web_xxx KWs for RFUI Framework
> * Offer some enhanced KWs, which have safe-loading and multiple actions
    Web Hover And Click   Web Click Text Button
> * All KWs works both in iOS and Android

-----
###  1.0.2 @2016.4.15
> * add New KWs
    web_wait_until_text_exist  web_wait_until_text_vanish web_wait_until_element_exist web_wait_until_element_vanish
    web_get_text_button_num
> * optimize the timeout/log/description of KWs
> * fix/optimize some bugs and KWs

-----
###  1.0.3 @2016.5.20
> * add New function 
    Support to generate one gif file for each test case with the flag(gen_gif_flag). 
    Library           Selenium2Library    gen_gif_flag=True  
    Note: Now only support in solo, can't used in mix with mobile(ios/android)
> * fix/optimize some bugs and KWs
    issues/11:  Web Click Text Button don't support Text with space(&nbsp;) 登&nbsp;录
    update the KW 'Web Hover And Click', add two optional parameters:elementToHover_selected_num=1, elementToClick_selected_num=1

-----
###  1.0.4 @2016.5.23
> * fix hot bugs(issues/3)
    a bug invoked by the new feature -gif

-----
###  1.0.5 @2016.5.26
> * optimize gif feature
    use diff flag for mobilelib(mobile_gif=true) & weblib(web_gif=true)
> * fix bug in 'Web Click Text Button'

###  1.0.6 @2016.5.30
> * fix a bug issues/18(RFUI import library failed,which lead to keyword search missing)

###  2.0.0 @2016.6.21
> * optimize gif feature
> * add two keywords: Web Get Element Attribute, Web Get Value
> * unify the release version to 2.0.0