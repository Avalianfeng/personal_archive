export interface PluginModuleMeta {
  id: string;
  name: string;
  version: string;
  uiExperience: 'form' | 'immersive' | 'compact';
  layers: Array<'objective' | 'personality'>;
}

export const PLUGIN_ROOT = 'plugins';
