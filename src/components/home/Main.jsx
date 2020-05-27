import React from "react";
import ItemSearch from "../common/ItemSearch";
import history from "../history";
import styled from "styled-components";
import breakpoint from "../breakpoint";

const Wrapper = styled.div`
  display: flex;
  flex-flow: column;
`

const WrapperWrapper = styled.div`
  ${breakpoint("lg")`
    padding: 0px 100px;  
  `}
`


const DonateBannerWrapper = styled.div`
  display: flex;
  flex-flow: row;
  margin-top: 50px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 10px;
`;

const DonateBannerText = styled.div`
  flex-grow: 1;
  display: flex;
  flex-flow: column;
  justify-content: center;
  padding: 30px;
`

const DonateButtonImageWrapper = styled.div`
  flex-grow: 0;
  > img {
    margin-right: 30px;
    margin-bottom: -3px;
    height: 275px;
    display: none;

    ${breakpoint("lg")`
      display: block;
    `}
  }

`

const DonateButtonButtonsWrapper = styled.div`
  display: flex;
  flex-flow: row;
`

const Button = styled.a`
  border: none;
  background: ${props => props.color};
  display: flex;
  flex-flow: row;
  align-items: center;
  border-radius: 8px;
  padding: 5px 10px;
  cursor: pointer;
  text-decoration: none;
  margin-left: ${props => props.margin}px;
`


const ButtonFont = styled.span`
  color: white;
  margin-left: 3px;
  letter-spacing: 1.1px;
  font-size: 17px;
  margin-left: 2px;
`


const Main = () => {
  const itemSearchCallback = (item) => {
    history.push(`/database/${item.table}/${item.code}`);
  }

  document.title = "Home";

  return (
    <Wrapper>
      <ItemSearch callback={itemSearchCallback} />

      <WrapperWrapper>
        <DonateBannerWrapper>
          <DonateBannerText>
            <h1>Welcome to Flandria!</h1>
            <p>If you like Flandria you can help us keep the site running by supporting us on PayPal or Patreon!</p>

            <DonateButtonButtonsWrapper>
              <Button margin={0} color="#085c8a" target="_blank" href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DWR39ZZHBKXAQ&source=url">
                <img src="https://www.paypalobjects.com/webstatic/icon/favicon.ico" />
                <ButtonFont>PayPal</ButtonFont>
              </Button>

              <Button margin={15} color="#f96853" target="_blank" href="https://www.patreon.com/Flandria">
                <img src="/static/assets/patreon.png" />
                <ButtonFont>Patreon</ButtonFont>
              </Button>

            </DonateButtonButtonsWrapper>
          </DonateBannerText>
          <DonateButtonImageWrapper>
            <img src="/static/assets/npc_portraits/p_meanjelro.png" />
          </DonateButtonImageWrapper>
        </DonateBannerWrapper>
      </WrapperWrapper>

    </Wrapper>
  )
}

export default Main;