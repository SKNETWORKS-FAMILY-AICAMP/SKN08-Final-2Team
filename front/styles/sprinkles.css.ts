import { defineProperties, createSprinkles } from '@vanilla-extract/sprinkles';

const sprinklesConfig = defineProperties({
  conditions: {
    small: {},
    medium: { '@media': 'screen and (min-width: 768px)' },
    large: { '@media': 'screen and (min-width: 1024px)' },
  },
  defaultCondition: 'small',
  properties: {
    display: ['none', 'block', 'flex'],
    flexDirection: ['row', 'column'],
    justifyContent: ['center', 'space-between'],
    alignItems: ['center', 'flex-start'],
    width: ['100%', 'auto'],
    height: ['100%', '600px', '800px'],
    padding: ['0', '8px', '16px'],
    margin: ['0', '8px', '16px'],
    backgroundColor: ['white', 'gray', 'blue'],
  },
});

export const sprinkles = createSprinkles(sprinklesConfig);
