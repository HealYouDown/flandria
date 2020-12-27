import React, { useEffect } from 'react';
import { setWindowTitle } from '../../helpers';
import Prose from '../shared/Prose';

const PrivacyPolicy = () => {
  useEffect(() => {
    setWindowTitle('Privacy Policy');
  }, []);

  return (
    <Prose>
      <h1 className="sr-only">Privacy Policy for www.flandria.info</h1>

      <h2>Privacy Policy</h2>
      <p>
        At Flandria, accessible from www.flandria.info, one of our main priorities is
        the privacy of our visitors. This Privacy Policy document contains types of
        information that is collected and recorded by Flandria and how we use it.
      </p>

      <p>
        If you have additional questions or require more information about our
        Privacy Policy, do not hesitate to contact us.
      </p>

      <p>
        This Privacy Policy applies only to our online activities and is valid
        for visitors to our website with regards to the information that they
        shared and/or collect in Flandria. This policy is not applicable to
        any information collected offline or via channels other than this
        website.
      </p>
      <blockquote>
        Our Privacy Policy was created with the help of the
        {' '}
        <a href="https://www.privacypolicygenerator.info">Privacy Policy Generator</a>
        {' '}
        and the
        {' '}
        <a href="https://www.privacypolicyonline.com">Free Privacy Policy Generator</a>
        .
      </blockquote>

      <h2>Consent</h2>
      <p>By using our website, you hereby consent to our Privacy Policy and agree to its terms.</p>

      <h2>How we use your information</h2>
      <p>We use the information we collect in various ways, including to:</p>
      <ul>
        <li>Provide, operate, and maintain our website</li>
        <li>Improve, personalize, and expand our website</li>
        <li>Understand and analyze how you use our website</li>
        <li>Develop new products, services, features, and functionality</li>
      </ul>

      <h2>Log Files</h2>
      <p>
        Flandria follows a standard procedure of using log files.
        These files log visitors when they visit websites. All hosting
        companies do this and a part of hosting services&apos; analytics.
        The information collected by log files include internet protocol
        (IP) addresses, browser type, Internet Service Provider (ISP),
        date and time stamp, referring/exit pages, and possibly the number
        of clicks. These are not linked to any information that is
        personally identifiable. The purpose of the information is for
        analyzing trends, administering the site, tracking users&apos;
        movement on the website, and gathering demographic information.
      </p>

      <h2>Cookies and Web Beacons</h2>
      <p>
        Like any other website, Flandria uses &apos;cookies&apos;.
        These cookies are used to store information including visitors&apos;
        preferences, and the pages on the website that the visitor accessed
        or visited. The information is used to optimize the users&apos;
        experience by customizing our web page content based on visitors&apos;
        browser type and/or other information.
      </p>

      <p>
        For more general information on cookies, please read
        {' '}
        <a href="https://www.cookieconsent.com/what-are-cookies/">&quot;What Are Cookies&quot; from Cookie Consent</a>
        .
      </p>

      <h2>Google DoubleClick DART Cookie</h2>
      <p>
        Google is one of a third-party vendor on our site. It also uses cookies,
        known as DART cookies, to serve ads to our site visitors based upon
        their visit to www.website.com and other sites on the internet.
        However, visitors may choose to decline the use of DART cookies
        by visiting the Google ad and content network Privacy Policy at the following URL –
        {' '}
        <a href="https://policies.google.com/technologies/ads">https://policies.google.com/technologies/ads</a>
      </p>

      <h2>Advertising Partners Privacy Policies</h2>
      <p>
        You may consult this list to find the Privacy Policy
        for each of the advertising partners of Flandria.

      </p>

      <p>
        Third-party ad servers or ad networks uses technologies like cookies,
        JavaScript, or Web Beacons that are used in their respective
        advertisements and links that appear on Flandria, which are
        sent directly to users&apos; browser. They automatically receive
        your IP address when this occurs. These technologies are used
        to measure the effectiveness of their advertising campaigns
        and/or to personalize the advertising content that you see
        on websites that you visit.
      </p>

      <p>
        Note that Flandria has no access to or control over
        these cookies that are used by third-party advertisers.
      </p>

      <h2>Third Party Privacy Policies</h2>

      <p>
        Flandria&apos;s Privacy Policy does not apply to other advertisers
        or websites. Thus, we are advising you to consult the
        respective Privacy Policies of these third-party ad
        servers for more detailed information. It may include
        their practices and instructions about how to opt-out
        of certain options.
      </p>

      <p>
        You can choose to disable cookies through your individual
        browser options. To know more detailed information about
        cookie management with specific web browsers, it can be
        found at the browsers&apos; respective websites.
      </p>

      <h2>
        GDPR Data Protection Rights /
        CCPA Privacy Rights (Do Not Sell My Personal Information)
      </h2>
      <p>
        If you want to edit, receive or have your data deleted, feel free to contact us.
        Please note that we may take up to a month to respond to you.
      </p>
    </Prose>
  );
};
export default PrivacyPolicy;
