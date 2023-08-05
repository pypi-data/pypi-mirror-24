import { registerPluginNamespace } from 'girder/pluginUtils';

import './routes';

// Extends and overrides API
import './views/HeaderUserView';
import './views/AdminView';

import * as jobs from './index';

registerPluginNamespace('jobs', jobs);
